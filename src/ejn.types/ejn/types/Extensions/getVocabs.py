from ejn.types.vocabs import site_themes
from ejn.types.vocabs import site_regions
from ejn.types.vocabs import ejn_programs
from ejn.types.vocabs import sharing_roles
from ejn.types.vocabs import occupations
from ejn.types.vocabs import media_types

def getVocabs(self):
  res = {}
  res['site_themes'] = site_themes
  res['site_regions'] = site_regions
  res['ejn_programs'] = ejn_programs
  res['sharing_roles'] = sharing_roles
  res['occupations'] = occupations
  res['media_types'] = media_types
  
  return res