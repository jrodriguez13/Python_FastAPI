#--------------------------------------------------------------#
#                  CLASE MODELO HABILIDADES                    #
#--------------------------------------------------------------#

from pydantic import BaseModel

class Skill(BaseModel):
    name: str
    years: int