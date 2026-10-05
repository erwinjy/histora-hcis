from __future__ import annotations
import httpx
from .contracts import RightsDecision

class LibraryOfCongressConnector:
    BASE="https://www.loc.gov"
    async def provider_info(self): return {"id":"loc_us","name":"Library of Congress"}
    async def health_check(self): return {"status":"READY"}
    async def search(self, query):
        params={"q":query.get("q",""),"fo":"json","c":query.get("limit",20)}
        async with httpx.AsyncClient(timeout=30) as c:
            r=await c.get(f"{self.BASE}/search/",params=params); r.raise_for_status()
            data=r.json()
        return data.get("results",[])
    async def get_item(self, external_id): raise NotImplementedError
    async def get_rights(self, candidate):
        return RightsDecision("RIGHTS_UNKNOWN",None,False,None,None,None,candidate.get("id"),"must parse item rights before download")
    async def download(self,candidate,target_path):
        raise PermissionError("download requires explicit RightsDecision.download_allowed=True")

class SmithsonianOpenAccessConnector:
    async def provider_info(self): return {"id":"smithsonian_oa"}
    async def health_check(self): return {"status":"TODO_API_KEY"}
    async def search(self,query): raise NotImplementedError
    async def get_item(self,external_id): raise NotImplementedError
    async def get_rights(self,candidate): raise NotImplementedError
    async def download(self,candidate,target_path): raise NotImplementedError

class EuropeanaConnector(SmithsonianOpenAccessConnector): pass
class GallicaConnector(SmithsonianOpenAccessConnector): pass
class NationalPalaceMuseumConnector(SmithsonianOpenAccessConnector): pass
class AcademiaSinicaDiscoveryConnector(SmithsonianOpenAccessConnector): pass
