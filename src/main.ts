import Eris from "eris";
import fs from "fs"
import path from "path"
import dotenv from 'dotenv'

//tutaj laduje sie dotenv
dotenv.config();


const bot = new Eris(process.env.TOKEN as string, {
intents:["guilds", "guildMessages", "messageContent", "guildMembers"]
});


bot.on("ready", () => {
    console.log("Super dziala");
});


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