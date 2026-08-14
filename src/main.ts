import Eris from "eris";
import fs from "fs"
import path from "path"
import dotenv from 'dotenv'

//tutaj laduje sie dotenv
dotenv.config();

//klient czy inne gowno
const bot = new Eris(process.env.TOKEN as string, {
intents:["guilds", "guildMessages", "messageContent", "guildMembers"]
});

//chyba uruchamianie
bot.on("ready", () => {
    console.log("Super dziala");

    bot.createCommand({
        name: "ping",
        description: "Ping command"
    });
});

//ping pong
bot.on("interactionCreate", interaction => {
    if (interaction.data.name === "ping") {
        const guildShard = bot.shards.get(0);
        const apiPing = guildShard ? Math.round(guildShard.latency) : 0;
        const startTime = Date.now();
        const interactionTime = interaction.createdAt;
        const botPing = startTime - interactionTime;
        //wiem ze to nie jest najlepsze ale dziala 👍
        interaction.createMessage("pong **" + botPing + "ms**");
    }
});

//to na pewno uruchamianie
bot.connect();