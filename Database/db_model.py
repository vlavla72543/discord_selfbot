from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class YtParser(Base):
    __tablename__ = 'YtParser'

    id = Column(Integer, primary_key=True)
    yt_channel = Column(String)
    ds_channel = Column(String)
    video_title = Column(String)
    video_url = Column(String)

    def __repr__(self):
        return f"YtParser(id={self.id!r}, yt_channel={self.yt_channel!r}, ds_channel={self.ds_channel!r}," \
               f"video_title={self.video_title!r}, video_url={self.video_url!r}"
