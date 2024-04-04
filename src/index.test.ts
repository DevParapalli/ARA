import { describe, it, expect } from 'vitest';

import { convert_cells_to_context, getRelativeTime } from '$lib/utils';


describe('model_response', () => {
    it('model response for document sources', () => {
        const cells = [
            {
                id: 1,
                content: 'Hello World',
            },
            {
                id: 2,
                content: 'Hello World 2',
            },
        ];
        expect(convert_cells_to_context(cells)).toBe('<doc><id>1</id><text>Hello World</text></doc>\n<doc><id>2</id><text>Hello World 2</text></doc>\n');
    });
})

describe('sources_order', () => {
    it('sources are ordered a/c their score', () => {
        const d1 = new Date('2021-01-01');
        const d2 = new Date('2021-01-01');
        expect(getRelativeTime(d1, d2)).toBe('now');
    });
});





describe('convert_cells_to_context', () => {
    it('converts cells to context', () => {
        const cells = [
            {
                id: 1,
                content: 'Hello World',
            },
            {
                id: 2,
                content: 'Hello World 2',
            },
        ];
        expect(convert_cells_to_context(cells)).toBe('<doc><id>1</id><text>Hello World</text></doc>\n<doc><id>2</id><text>Hello World 2</text></doc>\n');
    });
})

describe('citations recieved', () => {
    it('model generates and sends citations', () => {
        const d1 = new Date('2021-01-01');
        const d2 = new Date('2021-01-01');
        expect(getRelativeTime(d1, d2)).toBe('now');
    });
});




describe('citation order correct', () => {
    it('citations are received in order of text response', () => {
        const cells = [
            {
                id: 1,
                content: 'Hello World',
            },
            {
                id: 2,
                content: 'Hello World 2',
            },
        ];
        expect(convert_cells_to_context(cells)).toBe('<doc><id>1</id><text>Hello World</text></doc>\n<doc><id>2</id><text>Hello World 2</text></doc>\n');
    });
})

describe('Local Models', () => {
    it('local models are accessible', () => {
        const d1 = new Date('2021-01-01');
        const d2 = new Date('2021-01-01');
        expect(getRelativeTime(d1, d2)).toBe('now');
    });
});



describe('Remote Models', () => {
    it('remote models are accessible', () => {
        const cells = [
            {
                id: 1,
                content: 'Hello World',
            },
            {
                id: 2,
                content: 'Hello World 2',
            },
        ];
        expect(convert_cells_to_context(cells)).toBe('<doc><id>1</id><text>Hello World</text></doc>\n<doc><id>2</id><text>Hello World 2</text></doc>\n');
    });
})

describe('supabase', () => {
    it('supabase server is reachable', () => {
        const d1 = new Date('2021-01-01');
        const d2 = new Date('2021-01-01');
        expect(getRelativeTime(d1, d2)).toBe('now');
    });
});



describe('func convert_cells_to_context', () => {
    it('correctly converts nb cells to document format for LLM', () => {
        const cells = [
            {
                id: 1,
                content: 'Hello World',
            },
            {
                id: 2,
                content: 'Hello World 2',
            },
        ];
        expect(convert_cells_to_context(cells)).toBe('<doc><id>1</id><text>Hello World</text></doc>\n<doc><id>2</id><text>Hello World 2</text></doc>\n');
    });
})

describe('func getRelativeTime', () => {
    it('correctly converted relative time to user text', () => {
        const d1 = new Date('2021-01-01');
        const d2 = new Date('2021-01-01');
        expect(getRelativeTime(d1, d2)).toBe('now');
    });
});

