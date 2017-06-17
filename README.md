# latch
A web framework built around python asyncio, protobuf, and pub-sub.

### Overview
Latch is a framework that draws upon the ideas of gRPC and the microservices pattern more generally, and with inspiration from the Robot Operating System (ROS), with an emphasis on fault tolerance and elimination of single points of failure where possible.  There is no service discovery - the API gateway simply translates incoming requests into protobuf messages and publishes them to a queue.  The queue allows multiple consumption in an effort to reduce coupling between resources and services - multiple services may be involved in the preperation of particular resources, so each resource will be broadcast over the wire.  Also, each service is agnostic of all other services.  It may request additional internal resources, but may not request it from a specific service.

