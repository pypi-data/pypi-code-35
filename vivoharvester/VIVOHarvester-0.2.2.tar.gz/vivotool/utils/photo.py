import rdflib

from rdflib import Graph, Literal, BNode, RDF, RDFS, URIRef, Namespace
from rdflib.namespace import FOAF, DC


class Photo:

    def create_user_photo_graph(self, pid, eid):

        VITRO_PUBLIC = Namespace(
            "http://vitro.mannlib.cornell.edu/ns/vitro/public#")
        COLLAB_VT = Namespace("http://collab.vt.edu/vivo/individual/")

        user = COLLAB_VT[pid]
        userimage = COLLAB_VT[pid + '-image']
        imageDownload = COLLAB_VT[pid + '-imageDownload']
        imageThumbnail = COLLAB_VT[pid + '-imageThumbnail']
        imageThumbnailDownload = COLLAB_VT[pid + '-imageThumbnailDownload']

        thingURL = URIRef("http://www.w3.org/2002/07/owl#Thing")
        fileURL = URIRef(
            "http://vitro.mannlib.cornell.edu/ns/vitro/public#File")
        fileByteStreamURL = URIRef(
            "http://vitro.mannlib.cornell.edu/ns/vitro/public#FileByteStream")

        jpegmimeType = Literal("image/jpeg")
        filename = Literal(eid + ".jpeg")
        directDownloadUrl = Literal(
            "/harvestedImages/fullImages/" + eid + ".jpeg")
        thumbnailDownloadUrl = Literal(
            "/harvestedImages/thumbnails/" + eid + ".jpeg")

        g = Graph()

        g.bind('vitro-public', VITRO_PUBLIC)

        g.add((user, VITRO_PUBLIC.mainImage, userimage))

        g.add((userimage, RDF.type, thingURL))
        g.add((userimage, RDF.type, fileURL))
        g.add((userimage, VITRO_PUBLIC.downloadLocation, imageDownload))
        g.add((userimage, VITRO_PUBLIC.thumbnailImage, imageThumbnail))
        g.add((userimage, VITRO_PUBLIC.filename, filename))
        g.add((userimage, VITRO_PUBLIC.mimeType, jpegmimeType))

        g.add((imageDownload, RDF.type, fileByteStreamURL))
        g.add(
            (imageDownload,
             VITRO_PUBLIC.directDownloadUrl,
             directDownloadUrl))

        g.add((imageThumbnail, RDF.type, thingURL))
        g.add((imageThumbnail, RDF.type, fileURL))
        g.add(
            (imageThumbnail,
             VITRO_PUBLIC.downloadLocation,
             imageThumbnailDownload))
        g.add((imageThumbnail, VITRO_PUBLIC.filename, filename))
        g.add((imageThumbnail, VITRO_PUBLIC.mimeType, jpegmimeType))

        g.add((imageThumbnailDownload, RDF.type, fileByteStreamURL))
        g.add(
            (imageThumbnailDownload,
             VITRO_PUBLIC.directDownloadUrl,
             thumbnailDownloadUrl))

        return g.serialize(format='nt')
