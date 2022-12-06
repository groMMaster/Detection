from pullenti.unisharp.Misc import Stopwatch

from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.Sdk import Sdk


class Ner:
    def __init__(self):
        sw = Stopwatch()
        Sdk.initialize_all()
        sw.stop()


    @staticmethod
    def getNer(text):
        with ProcessorService.create_processor() as proc:
            ar = proc.process(SourceOfAnalysis(txt), None, None)
            for e0_ in ar.entities:
                print("{0}: {1}".format(e0_.type_name, str(e0_)), flush=True)
                for s in e0_.slots:
                    print("   {0}: {1}".format(s.type_name, s.value), flush=True)

txt = "Система разрабатывается с 2011 года российским программистом Михаилом Жуковым, проживающим в Москве на Красной площади в доме номер один на втором этаже. Конкурентов у него много: Abbyy, Yandex, ООО \"Russian Context Optimizer\" (RCO) и другие компании. Он планирует продать SDK за 1.120.000.001,99 (миллиард сто двадцать миллионов один рубль 99 копеек) рублей, без НДС."
a = Ner().getNer(txt)