from .usGaap.UsGaapHandler import UsGaapHandler

class TerminationHandler():
    
    def get_usGaap(cik: str):
        usGaapWrapper = {}
        usGaapWrapper["usGaap"] = UsGaapHandler.getUsGaapFacts(UsGaapHandler(), cik=cik)

        return [usGaapWrapper]
        
        