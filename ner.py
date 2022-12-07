from pullenti.unisharp.Misc import Stopwatch

from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.Sdk import Sdk


def NerInstall():
    sw = Stopwatch()
    Sdk.initialize_all()
    sw.stop()


def GetNer(file):
    with ProcessorService.create_processor() as proc:
        with open("res/ner.txt", "w") as ner:
            with open(file, "r") as segmentation:
                for txt in segmentation:
                    ar = proc.process(SourceOfAnalysis(txt), None, None)
                    for e0_ in ar.entities:
                        ner.write("{0}: {1}".format(e0_.type_name, str(e0_)) + '\n')
                        for s in e0_.slots:
                            ner.write("   {0}: {1}".format(s.type_name, s.value) + '\n')

NerInstall()
GetNer("res/segmentation.txt")