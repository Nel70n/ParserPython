from ParserGoogle import ParseLink

query = 'elon musk'


session = ParseLink(
    query=query
)

session.CreateResponse()
