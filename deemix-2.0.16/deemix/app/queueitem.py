class QueueItem:
    def __init__(self, id=None, bitrate=None, title=None, artist=None, cover=None, explicit=False, size=None, type=None, settings=None, queueItemDict=None):
        if queueItemDict:
            self.title = queueItemDict['title']
            self.artist = queueItemDict['artist']
            self.cover = queueItemDict['cover']
            self.explicit = queueItemDict.get('explicit', False)
            self.size = queueItemDict['size']
            self.type = queueItemDict['type']
            self.id = queueItemDict['id']
            self.bitrate = queueItemDict['bitrate']
            self.extrasPath = queueItemDict.get('extrasPath', '')
            self.files = queueItemDict['files']
            self.downloaded = queueItemDict['downloaded']
            self.failed = queueItemDict['failed']
            self.errors = queueItemDict['errors']
            self.progress = queueItemDict['progress']
            self.settings = queueItemDict.get('settings')
        else:
            self.title = title
            self.artist = artist
            self.cover = cover
            self.explicit = explicit
            self.size = size
            self.type = type
            self.id = id
            self.bitrate = bitrate
            self.extrasPath = None
            self.files = []
            self.settings = settings
            self.downloaded = 0
            self.failed = 0
            self.errors = []
            self.progress = 0
        self.uuid = f"{self.type}_{self.id}_{self.bitrate}"
        self.cancel = False
        self.ack = None

    def toDict(self):
        return {
            'title': self.title,
            'artist': self.artist,
            'cover': self.cover,
            'explicit': self.explicit,
            'size': self.size,
            'extrasPath': self.extrasPath,
            'files': self.files,
            'downloaded': self.downloaded,
            'failed': self.failed,
            'errors': self.errors,
            'progress': self.progress,
            'type': self.type,
            'id': self.id,
            'bitrate': self.bitrate,
            'uuid': self.uuid,
            'ack': self.ack
        }

    def getResettedItem(self):
        item = self.toDict()
        item['downloaded'] = 0
        item['failed'] = 0
        item['progress'] = 0
        item['errors'] = []
        return item

    def getSlimmedItem(self):
        light = self.toDict()
        propertiesToDelete = ['single', 'collection', '_EXTRA', 'settings']
        for property in propertiesToDelete:
            if property in light:
                del light[property]
        return light

class QISingle(QueueItem):
    def __init__(self, id=None, bitrate=None, title=None, artist=None, cover=None, explicit=False, type=None, settings=None, single=None, queueItemDict=None):
        if queueItemDict:
            super().__init__(queueItemDict=queueItemDict)
            self.single = queueItemDict['single']
        else:
            super().__init__(id, bitrate, title, artist, cover, explicit, 1, type, settings)
            self.single = single

    def toDict(self):
        queueItem = super().toDict()
        queueItem['single'] = self.single
        return queueItem

class QICollection(QueueItem):
    def __init__(self, id=None, bitrate=None, title=None, artist=None, cover=None, explicit=False, size=None, type=None, settings=None, collection=None, queueItemDict=None):
        if queueItemDict:
            super().__init__(queueItemDict=queueItemDict)
            self.collection = queueItemDict['collection']
        else:
            super().__init__(id, bitrate, title, artist, cover, explicit, size, type, settings)
            self.collection = collection

    def toDict(self):
        queueItem = super().toDict()
        queueItem['collection'] = self.collection
        return queueItem

class QIConvertable(QICollection):
    def __init__(self, id=None, bitrate=None, title=None, artist=None, cover=None, explicit=False, size=None, type=None, settings=None, extra=None, queueItemDict=None):
        if queueItemDict:
            super().__init__(queueItemDict=queueItemDict)
            self.extra = queueItemDict['_EXTRA']
        else:
            super().__init__(id, bitrate, title, artist, cover, explicit, size, type, settings, [])
            self.extra = extra

    def toDict(self):
        queueItem = super().toDict()
        queueItem['_EXTRA'] = self.extra
        return queueItem
