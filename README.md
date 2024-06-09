# BreadNet Specification

## Protocol Objectives

BreadNet aims to be a universal text transfer protocol designed to run on a given BreadNet Network for simple text based communication across various applications.

## Packet Format (Version 100)

### Generic Requests

Here is an example in the form of a Sprintf function from golang

```
fmt.Sprintf("breadnet 100\n%s\n\n%s\n", requestType, content)
```

### Generic Responses

Here is an example in the form of a Sprintf function from golang

```
fmt.Sprintf("breadnet 100\n%d\n\n%s", statusCode, content)
```

## Communication Model

BreadNet operates over TCP/IP and relies on the developer to specify whether the connection should be peer-to-peer or client-server (similar to http) based on the applicaton's needs. The supported version 100 spec request types are as follows:

- `get`: Ask for a response from the server

## Error Handling

Errors are communicated in the response header in the `statusCode` field. Codes for the 100 spec are as follows

- `100`: OK
- `200`: BAD

## Security

BreadNet does not include built-int security features. This might be something I work on as the protocol matures.

## Performace Metrics

The protocol does not define certain performace requirements.

## Compatibility and Interoperability

BreadNet is a standalone protocol and does not ensure compatibility with earlier or later versions of the protocol. More to come on this as the protocol matures.

## Versioning and Updates

Versioning is managed through the packet header. Documentation for different versions of the protocol is maintained on seperate branches in the GitHub repository, with the main branch hosting the current specification.
