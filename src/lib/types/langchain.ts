import type { Document } from "@langchain/core/documents";

export interface RemoteRunnableResponseChunk {
    'run_id': string;
    'prompt': string;
    'context': string;
    'response': string;
    'sources': Document[];
    
}

export type RemoteRunnableResponse = RemoteRunnableResponseChunk[];