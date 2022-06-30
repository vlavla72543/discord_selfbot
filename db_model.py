from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class YtParser(Base):
    __tablename__ = 'YtParser'

    id = Column(Integer, primary_key=True)
    yt_channel = Column(String)
    ds_channel = Column(String)
    video_title = Column(String)
    video_url = Column(String)



