import fs from "fs";
import path from "path";
import url from "url";

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

export default class Lang {
    private lang: string;
    private filePath: string;
    private data: Record<string, string> = {};

    constructor(lang: string) {
        this.lang = lang.toLowerCase(); // EN → en, PL → pl
        this.filePath = path.join(__dirname, "..", "langs", `${this.lang}.json`);

        // Jeśli plik nie istnieje → utwórz pusty JSON
        if (!fs.existsSync(this.filePath)) {
            fs.writeFileSync(this.filePath, "{}");
        }

        // Wczytaj JSON
        try {
            const raw = fs.readFileSync(this.filePath, "utf8");
            this.data = raw.trim() === "" ? {} : JSON.parse(raw);
        } catch {
            // Jeśli plik jest uszkodzony → napraw
            this.data = {};
            fs.writeFileSync(this.filePath, "{}");
        }
    }

    L(key: string): string | null {
        return this.data[key] ?? null;
    }
}
