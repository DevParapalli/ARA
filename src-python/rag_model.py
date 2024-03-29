from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union

import ujson
from cohere import ChatCitation, ChatSearchQuery, ChatSearchResult
from langchain_cohere import ChatCohere
from langchain_core.callbacks.manager import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain_core.messages import AIMessage, BaseMessage, ChatMessage, HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.outputs.chat_generation import ChatGenerationChunk


def get_role(message: BaseMessage) -> str:
    """Get the role of the message.

    Args:
        message: The message.

    Returns:
        The role of the message.

    Raises:
        ValueError: If the message is of an unknown type.
    """
    if isinstance(message, ChatMessage) or isinstance(message, HumanMessage):
        return "User"
    elif isinstance(message, AIMessage):
        return "Chatbot"
    elif isinstance(message, SystemMessage):
        return "System"
    else:
        raise ValueError(f"Got unknown type {message}")


def get_cohere_chat_request(
    messages: List[BaseMessage],
    *,
    connectors: Optional[List[Dict[str, str]]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Get the request for the Cohere chat API.

    Args:
        messages: The messages.
        connectors: The connectors.
        **kwargs: The keyword arguments.

    Returns:
        The request for the Cohere chat API.
    """
    documents = (
        None
        if "source_documents" not in kwargs
        else [
            {
                "snippet": doc.page_content,
                "id": doc.metadata.get("id") or f"doc-{str(i)}",
            }
            for i, doc in enumerate(kwargs["source_documents"])
        ]
    )
    kwargs.pop("source_documents", None)
    maybe_connectors = connectors if documents is None else None

    # by enabling automatic prompt truncation, the probability of request failure is
    # reduced with minimal impact on response quality
    prompt_truncation = "AUTO" if documents is not None or connectors is not None else None

    req = {
        "message": messages[-1].content,
        "chat_history": [{"role": get_role(x), "message": x.content} for x in messages[:-1]],
        "documents": documents,
        "connectors": maybe_connectors,
        "prompt_truncation": prompt_truncation,
        **kwargs,
    }

    return {k: v for k, v in req.items() if v is not None}


def convert_citations_to_dict(citations: List[ChatCitation], **kwargs) -> List[Dict[str, Union[str, int, List[str]]]]:
    # kwargs_with_defaults = {"by_alias": True, "exclude_unset": True, **kwargs}
    if not citations:
        return []
    return [
        {"start": citation.start, "end": citation.end, "text": citation.text, "document_ids": citation.document_ids}
        for citation in citations
    ]


def convert_search_queries_to_dict(search_queries: List[ChatSearchQuery], **kwargs):
    if not search_queries:
        return []
    return [{"query": search_query.text} for search_query in search_queries]


_cohere_document = {
    "id": "doc-0",  # usually web-search_x
    "snippet": "This is a snippet of the document.",  # This is the text to be referenced
    "timestamp": "2022-01-01T00:00:00",  # This is the time the document was search in UTC time
    "title": "Document Title",  # This is the title of the document
    "url": "https://example.com",  # This is the URL of the source
}


def convert_chat_search_results_to_dict(search_results: List[ChatSearchResult], **kwargs):
    if not search_results:
        return []
    return [
        {
            "connector": search_result.connector.id,
            # 'documents': search_result.documents if len(search_result.document_ids) > 0 else [], #type:ignore documents is maybe defined, so we check ids for presence
            "document_ids": search_result.document_ids,
        }
        for search_result in search_results
    ]


def serialize(data: Any) -> str:
    return ujson.dumps(data)


class ChatCohereWithMetadata(ChatCohere):
    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        request = get_cohere_chat_request(messages, **self._default_params, **kwargs)

        if hasattr(self.client, "chat_stream"):  # detect and support sdk v5
            stream = self.client.chat_stream(**request)
        else:
            stream = self.client.chat(**request, stream=True)

        for data in stream:
            # print(data)
            if data.event_type == "text-generation":
                delta = data.text
                chunk = ChatGenerationChunk(message=AIMessageChunk(content=delta))
                if run_manager:
                    run_manager.on_llm_new_token(delta, chunk=chunk)
                yield chunk
            if data.event_type == "citation-generation":
                chunk = ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=f"__citation__:{serialize(convert_citations_to_dict(data.citations))}"
                    )
                )
                yield chunk
            if data.event_type == "search-queries-generation":
                chunk = ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=f"__search_queries__:{serialize(convert_search_queries_to_dict(data.search_queries))}"
                    )
                )
                yield chunk
            if data.event_type == "search-results":
                chunk = ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=f"__search_results__:{serialize({'documents': data.documents, 'metadata': convert_chat_search_results_to_dict(data.search_results)})}"
                    )
                )
                yield chunk
            if data.event_type == "stream-end":
                chunk = ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=f"__stream_end__:{serialize({'token_count': data.response.token_count, 'metadata': data.response.meta})}"
                    )
                )
                yield chunk

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        request = get_cohere_chat_request(messages, **self._default_params, **kwargs)

        if hasattr(self.async_client, "chat_stream"):  # detect and support sdk v5
            stream = self.async_client.chat_stream(**request)
        else:
            stream = self.async_client.chat(**request, stream=True)

        async for data in stream:
            if data.event_type == "text-generation":
                delta = data.text
                chunk = ChatGenerationChunk(message=AIMessageChunk(content=delta))
                if run_manager:
                    await run_manager.on_llm_new_token(delta, chunk=chunk)
                yield chunk
            if data.event_type == "citation-generation":
                chunk = ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=f"__citation__:{serialize(convert_citations_to_dict(data.citations))}"
                    )
                )
                yield chunk
            if data.event_type == "search-queries-generation":
                chunk = ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=f"__search_queries__:{serialize(convert_search_queries_to_dict(data.search_queries))}"
                    )
                )
                yield chunk
            if data.event_type == "search-results":
                chunk = ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=f"__search_results__:{serialize({'documents': data.documents, 'metadata': convert_chat_search_results_to_dict(data.search_results)})}"
                    )
                )
                yield chunk
            if data.event_type == "stream-end":
                chunk = ChatGenerationChunk(
                    message=AIMessageChunk(
                        content=f"__stream_end__:{serialize({'token_count': data.response.token_count, 'metadata': data.response.meta})}"
                    )
                )
                yield chunk


# if data.event_type == "stream-end":
#     chunk = ChatGenerationChunk(message=AIMessageChunk(response_metadata={'documents':data.response.documents or [], 'citations':convert_citations_to_dict(data.response.citations)},
#                                                        additional_kwargs= {'documents':data.response.documents or [], 'citations':convert_citations_to_dict(data.response.citations)},
#                                                        content=json.dumps(
#                                                            {'documents':data.response.documents or [], 'citations':convert_citations_to_dict(data.response.citations)}
#                                                        )))
#     yield chunk
