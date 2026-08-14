import { execSync } from "child_process";

function checkAndPush() {
    try {
        // pobierz stan z remote
        execSync("git fetch", { stdio: "ignore" });

        // lokalny HEAD
        const local = execSync("git rev-parse HEAD").toString().trim();

        // upstream HEAD (origin/main lub origin/master)
        const remote = execSync("git rev-parse @{u}").toString().trim();

        if (local !== remote) {
            console.log("[AUTO-PUSH] Wykryto niepushnięte zmiany → pushuję...");
            execSync("git push", { stdio: "inherit" });
            console.log("[AUTO-PUSH] Push zakończony.");
        } else {
            console.log("[AUTO-PUSH] Repo jest zsynchronizowane.");
        }

    } catch (err) {
        console.error("[AUTO-PUSH] Błąd:", err.message);
    }
}

// sprawdzaj co 5 sekund
setInterval(checkAndPush, 5000);

console.log("AutoPush działa — sprawdzam repo co 5 sekund...");
