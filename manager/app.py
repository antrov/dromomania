# from config import get_config
from logger import log
from concurrent import futures

import grpc
import hashes
from grpc_reflection.v1alpha import reflection
from manager_pb2 import DESCRIPTOR, AddOfferRequest, AddOfferResponse, Status
from manager_pb2_grpc import (ManagerServiceServicer,
                              add_ManagerServiceServicer_to_server)
from models import Offer, OfferGroup, init_db

MAX_HASH_DIFFERENCE = 13
DEBUG = True


class RouteGuideServicer(ManagerServiceServicer):
    def AddOffer(self, request: AddOfferRequest, context):
        id = hashes.get_url_hash(request.image_url)[:6]
        log.info(f'{id} New image url {request.image_url}')
        try:
            Offer.get(Offer.image_url == request.image_url)
        except Offer.DoesNotExist:
            pass
        else:
            log.debug(f'{id} Offer with image url exists in db')
            return AddOfferResponse(status=Status.CONFLICT)

        try:
            img_hash = hashes.get_remote_img_hash(request.image_url)
            Offer.get(Offer.image_hash == img_hash)
        except Offer.DoesNotExist:
            pass
        else:
            log.debug(f'{id} Offer with image hash {img_hash} exists in db')
            return AddOfferResponse(status=Status.CONFLICT)

        existing_hashes = list(
            map(lambda o: o.image_hash, Offer.select(Offer.image_hash)))
        nearest_hash = hashes.get_min_diff(
            img_hash, existing_hashes, MAX_HASH_DIFFERENCE)

        if nearest_hash is None:
            log.debug(f'{id} No matching image found. Creating group')
            group = OfferGroup.create(
                offer_url=request.offer_url,
                title=request.title,
                params=request.params,
                tag=request.tag,
            )
        else:
            log.debug(f'{id} Matching offer and group found')
            group = Offer.get(Offer.image_hash == nearest_hash).group

        Offer.create(
            image_hash=img_hash,
            image_url=request.image_url,
            group=group
        )
        log.info(f'{id} Created offer {img_hash} in group {group.id}')

        return AddOfferResponse(status=Status.CREATED)


# allow running from the command line
if __name__ == '__main__':
    init_db()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ManagerServiceServicer_to_server(
        RouteGuideServicer(), server)

    if DEBUG:
        SERVICE_NAMES = (
            DESCRIPTOR.services_by_name['ManagerService'].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
