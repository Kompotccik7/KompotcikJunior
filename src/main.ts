import Eris, { Constants } from "eris";
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

    bot.createCommand({
        name: "ping",
        description: "Ping command"
    });

    bot.createCommand({
        name: "clear",
        description: "Clears chat",
        options:[
            {
                name: "amount",
                type: Constants.ApplicationCommandOptionTypes.INTEGER,
                description: "amount",
                required: true
            }
        ]
    });
});

bot.on("interactionCreate", async (interaction) => {
    //ping
    if (interaction.data.name === "ping") {
        const guildShard = bot.shards.get(0);
        const apiPing = guildShard ? Math.round(guildShard.latency) : 0;
        const startTime = Date.now();
        const interactionTime = interaction.createdAt;
        const botPing = startTime - interactionTime;
        //wiem ze to nie jest najlepsze ale dziala 👍
        interaction.createMessage("pong **" + botPing + "ms**");
    }
    //clear
    if (interaction.data.name === "clear") {
        await interaction.defer(64);
        const iloscopcja = interaction.data.options?.find(opt=>opt.name === "amount");
        const amount = iloscopcja?.value as number;

        try{
            const usunietewiadomosci = await bot.purgeChannel(interaction.channelID, {
                limit: amount,
                filterOld: true
            });
            await interaction.createFollowup({
                content:'super dziala',
                flags: 64
            });
        }
        catch (err){
            console.error(err)
        }
    }
});




//to na pewno uruchamianie
bot.connect();