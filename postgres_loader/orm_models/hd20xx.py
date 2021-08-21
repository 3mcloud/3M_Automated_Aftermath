from sqlalchemy import Column, Integer, Float, Text

from .constants import Base

class HD20XX(Base):
    """
    Model for IPEDS HD20XX table
    """
    __tablename__ = 'hd20xx'
    id = Column(Integer, primary_key = True)
    reporting_year = Column(Integer, nullable=False, comment="reporting year for record")
    unitid = Column(Integer, comment="Institution unit ID")
    instnm = Column(Text, comment="Institution (entity) name")
    ialias = Column(Text, comment="Institution name alias")
    stabbr = Column(Text, comment="State abbreviation")
    fips = Column(Integer, comment="FIPS state code")
    obereg = Column(Integer, comment="Bureau of Economic Analysis (BEA) regions")
    sector = Column(Integer, comment="Sector of institution")
    iclevel = Column(Integer, comment="Level of institution")
    control = Column(Integer, comment="Control of institution")
    hdegofr1 = Column(Integer, comment="Highest degree offered")
    hbcu = Column(Integer, comment="Historically Black College or University")
    hospital = Column(Integer, comment="Institution has hospital")
    medical = Column(Integer, comment="Institution grants a medical degree")
    tribal = Column(Integer, comment="Tribal college")
    locale = Column(Integer, comment="Degree of urbanization (Urban-centric locale)")
    newid = Column(Integer, comment="UNITID for merged schools")
    cyactive = Column(Integer, comment="Institution is active in current year")
    instcat = Column(Integer, comment="Institutional category")
    landgrnt = Column(Integer, comment="Land Grant Institution")
    instsize = Column(Integer, comment="Institution size category")
    
