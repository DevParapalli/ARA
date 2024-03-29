import type { Document } from '@langchain/core/documents';

export interface RemoteRunnableResponseChunk {
    run_id: string;
    prompt: string;
    context: string;
    response: string;
    sources: Document[];
}

export type RemoteRunnableResponse = RemoteRunnableResponseChunk[];

export interface LCSource {
    id: string;
    url: string;
    title: string;
    snippet: string;
    timestamp: string;
}
