import type { Tables } from './supabaseTypes';

function convert_cells_to_context(cells: Tables<'cells'>[]): string {
    let context = '';
    cells.forEach((cell) => {
        context += '<doc>' + `<id>${cell.id}</id>` + `<text>${cell.content}</text>` + '</doc>\n';
    });
    return context;
}

const units = {
    year: 24 * 60 * 60 * 1000 * 365,
    month: (24 * 60 * 60 * 1000 * 365) / 12,
    day: 24 * 60 * 60 * 1000,
    hour: 60 * 60 * 1000,
    minute: 60 * 1000,
    second: 1000,
};

const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });

const getRelativeTime = (d1: Date, d2: Date = new Date()) => {
    const elapsed = d1.valueOf() - d2.valueOf();

    // "Math.abs" accounts for both "past" & "future" scenarios
    for (const u in units)
        if (Math.abs(elapsed) > units[u] || u == 'second') return rtf.format(Math.round(elapsed / units[u]), u);
};

export { convert_cells_to_context, getRelativeTime };
