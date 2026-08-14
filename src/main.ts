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
});

//ping
bot.createCommand({
    name: "ping",
    description: "Ping command",
    type: 1
});

bot.on("interactionCreate", interaction => {
    if (interaction.data.name === "ping") {
        interaction.createMessage("pong");
    }
});

//to na pewno uruchamianie
bot.connect();