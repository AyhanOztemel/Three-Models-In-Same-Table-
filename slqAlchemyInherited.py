
from sqlalchemy import create_engine, Column, Integer, String,ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class BuildingInfoRecordModel(Base):
    __tablename__ = 'buildingInfoRecordDatabase'
    dbBuildingInfoId = Column(Integer, primary_key=True, autoincrement=True)
    dbBuildingInfoType = Column(String)  # This column will store the type of the record ('apart' or 'site')
    dbBuildingInfoName = Column(String)
    dbBuildingInfoCity = Column(String)
    dbBuildingInfoDistrict = Column(String)
    dbBuildingInfoNeighborhood = Column(String)
    dbBuildingInfoAvenue = Column(String)
    dbBuildingInfoStreet = Column(String)
    dbBuildingInfoNumber = Column(String)
    dbBuildingInfoExplanation = Column(String)
   
    __mapper_args__ = {
        'polymorphic_on': dbBuildingInfoType,
        'polymorphic_identity': 'building_info_record'
    }

class ApartBuildingInfoRecordModel(BuildingInfoRecordModel):
    __tablename__ = 'apartBuildingInfoRecordDatabase'
    dbBuildingInfoApartId = Column(Integer,ForeignKey('buildingInfoRecordDatabase.dbBuildingInfoId'), primary_key=True, autoincrement=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'apart_building_info_record',
        'inherit_condition': dbBuildingInfoApartId == BuildingInfoRecordModel.dbBuildingInfoId
    }

class SiteBuildingInfoRecordModel(BuildingInfoRecordModel):
    __tablename__ = 'siteBuildingInfoRecordDatabase'
    dbBuildingInfoSiteId = Column(Integer,ForeignKey('buildingInfoRecordDatabase.dbBuildingInfoId'), primary_key=True, autoincrement=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'site_building_info_record',
        'inherit_condition': dbBuildingInfoSiteId == BuildingInfoRecordModel.dbBuildingInfoId
    }

# create a engine
engine = create_engine('sqlite:///mydatabase2.db', echo=False)#echo=True)
#engine = create_engine('sqlite:///:memory:') you can use inmemory database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
#------------------------------------------add operations-----------------------------------
buildingInfoRecordModel=BuildingInfoRecordModel(dbBuildingInfoName="Alibey2",dbBuildingInfoCity="Ankara")

apartBuildingInfoRecordModel=ApartBuildingInfoRecordModel(dbBuildingInfoType ="apart_building_info_record",dbBuildingInfoName="delikız",dbBuildingInfoCity="İstanbul2")

siteBuildingInfoRecordModel= SiteBuildingInfoRecordModel(dbBuildingInfoType ="site_building_info_record",dbBuildingInfoName="Ayşehanım2",dbBuildingInfoCity="İzmir2")

session.add_all([buildingInfoRecordModel,apartBuildingInfoRecordModel, siteBuildingInfoRecordModel])
session.commit()

#------------------------------------------guery examples -----------------------------------
print("------ApartBuildingInfoRecordModel----gueryALL---------------------")
apartment_buildings = session.query(ApartBuildingInfoRecordModel).all()
for building in apartment_buildings:
    print(f"ID: {building.dbBuildingInfoId}, Units: {building.dbBuildingInfoName}")
print("----------------------------------------------------------------------------")

print("------SiteBuildingInfoRecordModel----gueryALL---------------------")
apartment_buildings = session.query(SiteBuildingInfoRecordModel).all()
for building in apartment_buildings:
    print(f"ID: {building.dbBuildingInfoId}, Units: {building.dbBuildingInfoName}")
print("----------------------------------------------------------------------------")

print("------BuildingInfoRecordModel----gueryALL for Alibey2---------------------")
query1 = session.query(BuildingInfoRecordModel).filter_by(dbBuildingInfoName='Alibey2').first()
print(f"Table1 - Name: {query1.dbBuildingInfoName} id:{query1.dbBuildingInfoId}")
print("----------------------------------------------------------------------------")

print("------BuildingInfoRecordModel----gueryALL ---------------------------------")
query2 = session.query(BuildingInfoRecordModel).all()#.filter_by(dbBuildingInfoName='delikız').all()
for building in query2:
    print(f"ID: {building.dbBuildingInfoId}, Units: {building.dbBuildingInfoName}")
print("Database created")
print("----------------------------------------------------------------------------")
