from sqlalchemy import Column, Integer, Float

from .constants import Base

class C20XX_C(Base):
    """
    Model for IPEDS C20XX_C table
    """
    __tablename__ = 'c20xx_C'
    id = Column(Integer, primary_key = True)
    reporting_year = Column(Integer, nullable=False, comment="reporting year for record")
    unitid = Column(Integer, comment="Institution unit ID")
    awlevelc = Column(Integer, comment="Award Level code")
    cstotlt = Column(Integer, comment="Grand total")
    cstotlm = Column(Integer, comment="Grand total men")
    cstotlw = Column(Integer, comment="Grand total women")
    csaiant = Column(Integer, comment="American Indian or Alaska Native total")
    csasiat = Column(Integer, comment="Asian total")
    csbkaat = Column(Integer, comment="Black or African American total")
    cshispt = Column(Integer, comment="Hispanic or Latino total")
    csnhpit = Column(Integer, comment="Native Hawaiian or Other Pacific Islander total")
    cswhitt = Column(Integer, comment="White total")
    cs2mort = Column(Integer, comment="Two or more races total")
    csunknt = Column(Integer, comment="Race/ethnicity unknown total")
    csnralt = Column(Integer, comment="Nonresident alien total")
    csund18 = Column(Integer, comment="Ages, under 18")
    cs18_24 = Column(Integer, comment="Ages, 18-24")
    cs25_39 = Column(Integer, comment="Ages, 25-39")
    csabv40 = Column(Integer, comment="Ages, 40 and above")
    csunkn = Column(Integer, comment="Age unknown")