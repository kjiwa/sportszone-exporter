"""Mappings from Sportszone to Team Cowboy attribute values."""

_GSHL_ID = 9941

class Translator(object):
  """Mappings of Sportszone attributes."""

  def __init__(self):
    """Creates a new translator."""
    self._arena = {}

  @property
  def arena(self):
    """Returns a mapping of arena names.

    Returns:
      A dict of arena names.
    """
    return self._arena

class GshlTranslator(Translator):
  """Mappings for GSHL attributes."""

  def __init__(self):
    """Creates a translator with GSHL attribute mappings."""
    super(GshlTranslator, self).__init__()
    self.arena['Castle'] = 'Castle Ice Arena'
    self.arena['Everett'] = 'Everett Events Center (Community Ice)'
    self.arena['Evt Main'] = 'Everett Events Center (Main Ice)'
    self.arena['Kent'] = 'Kent Valley Ice Center'
    self.arena['Kngsgate'] = 'Kingsgate Ice Arena'
    self.arena['Lynnwood'] = 'Lynnwood Ice Center'
    self.arena['Olympic'] = 'Olympic View Arena'
    self.arena['Showare'] = 'Showare Arena'

def load(name=None):
  """Loads a profile by league_id. Loads the default if there is no match.

  Args:
    league_id: The profile's league_id.

  Returns:
    A profile or the default if one could not be found.
  """
  return GshlTranslator() if name == _GSHL_ID else Translator()
