import fs from "fs";
import path from "path";
import url from "url";

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

export default class Config {
    private id: string;
    private filePath: string;
    private data: Record<string, boolean | string | number>;

    constructor(id: string) {
        this.id = id;
        this.filePath = path.join(__dirname, "..", "data", `${this.id}.json`);

        if (!fs.existsSync(this.filePath)) {
            fs.writeFileSync(this.filePath, "{}");
        }

        try {
            const raw = fs.readFileSync(this.filePath, "utf8");
            this.data = raw.trim() === "" ? {} : JSON.parse(raw);
        } catch {
            this.data = {};
            fs.writeFileSync(this.filePath, "{}");
        }
    }

    Get(key: string): boolean | string | number | null {
        return this.data[key] ?? null;
    }

    Set(key: string, value: boolean | string | number): void {
        this.data[key] = value;
        fs.writeFileSync(this.filePath, JSON.stringify(this.data, null, 2));
    }
}
