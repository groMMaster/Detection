from pullenti.unisharp.Misc import Stopwatch

from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.Sdk import Sdk


def NerInstall():
    sw = Stopwatch()
    Sdk.initialize_all()
    sw.stop()


def GetNer(text):
    entities = []
    with ProcessorService.create_processor() as proc:
        for txt in text:
            ar = proc.process(SourceOfAnalysis(txt), None, None)
            for i, e0_ in enumerate(ar.entities):
                entities.append({})
                entities[i][e0_.type_name] = str(e0_)

    return entities
