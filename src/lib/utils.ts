import type { Tables } from './supabaseTypes';

function convert_cells_to_context(cells: Tables<'cells'>[]): string {
    let context = '';
    cells.forEach((cell) => {
        context += '<doc>' + `<id>${cell.id}</id>` + `<text>${cell.content}</text>` + '</doc>\n';
    });
    return context;
}

export { convert_cells_to_context };
