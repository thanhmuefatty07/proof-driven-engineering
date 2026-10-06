class Gateway:
    def __init__(self, documents):
        self.documents = documents
        self.cache = {}

    def get_document(self, principal, tenant, document_id):
        if document_id in self.cache:
            return self.cache[document_id]
        if principal["tenant"] != tenant:
            raise PermissionError("Access denied")
        for document in self.documents:
            if document["id"] == document_id:
                self.cache[document_id] = document
                return document
        raise LookupError("Document not found")
