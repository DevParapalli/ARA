import type { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
    webServer: [
        {
            command: 'npm run build && npm run preview',
            port: 4173,
        },
        {
            command: 'cd src-python && python main.py',
            port: 4945,
            reuseExistingServer: true,
        }
    ],
    use: {
        baseURL: 'http://localhost:4173',
    },
    testDir: 'tests',
    testMatch: /(.+\.)?(test|spec)\.[jt]s/,
};

export default config;
