import flask
from flask import Flask, render_template, send_from_directory, url_for, request
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from segmentation import getSegmentation, startSegmentation
from ner import GetNer, NerInstall
from paddleocr import PPStructure

PP_TABLE_ENGINE = {}
ENGINE_INSTALLED = False

app = Flask(__name__)
app.config['UPLOADED_DOCUMENTS_DEST'] = 'docs'
app.config['SECRET_KEY'] = 'ac90825480812ea4e02bc39aceaa80e1'

documents = UploadSet('documents', IMAGES)
configure_uploads(app, documents)


class UploadForm(FlaskForm):
    doc = FileField(
        validators=[
            FileAllowed(documents, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')


@app.route('/docs/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_DOCUMENTS_DEST'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if request.method == "GET":

        return render_template('index.html', form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            filename = documents.save(form.doc.data)
            file_url = url_for('get_file', filename=filename)

            # Doc recognition
            res_img, detect_str, detect_table = getSegmentation(filename, PP_TABLE_ENGINE)
            ner_entities = GetNer(detect_str)

            html_tables = []
            for table in detect_table:
                html_tables.append(flask.Markup(table))

        else:
            filename = None
            file_url = None

        return render_template('result.html', form=form, filename=filename, file_url=file_url, res_img=res_img,
                               det_str=detect_str, ner_ent=ner_entities, det_table=html_tables)


if __name__ == '__main__':
    if not ENGINE_INSTALLED:
        startSegmentation()
        NerInstall()
        PP_TABLE_ENGINE = PPStructure(table=True, layout=True, show_log=True, ocr=False)
        ENGINE_INSTALLED = True

    app.run(debug=False)

