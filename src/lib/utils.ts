import type { Tables } from './supabaseTypes';

function convert_cells_to_context(cells: Tables<'cells'>[]): string {
    let context = '';
    cells.forEach((cell) => {
        context +=
            '<document>' +
            `<id>${cell.id}</id>` +
            `<document_content>${cell.content}</document_content>` +
            '</document>\n';
    });
    return context;
}

export { convert_cells_to_context };