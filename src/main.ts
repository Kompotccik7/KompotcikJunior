import Eris, { Constants } from "eris";
import fs from "fs";
import path from "path";
import dotenv from "dotenv";

dotenv.config();

const bot = new Eris(process.env.TOKEN as string, {
    intents: ["guilds", "guildMessages", "messageContent", "guildMembers"]
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
        options: [
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

    // ============================
    // PING
    // ============================
    if (interaction.data.name === "ping") {
        const shard = bot.shards.get(0);
        const apiPing = shard ? Math.round(shard.latency) : 0;

        const botPing = Date.now() - interaction.createdAt;

        interaction.createMessage(`pong **${botPing}ms**`);
    }

    // ============================
    // CLEAR
    // ============================
    if (interaction.data.name === "clear") {

        // EPHEMERAL DEFER
        await interaction.defer(64);

        const amountOpt = interaction.data.options?.find(opt => opt.name === "amount");
        const amount = amountOpt?.value as number;

        try {
            const deleted = await bot.purgeChannel(interaction.channelID, {
                limit: amount,
                filterOld: true
            });

            await interaction.createFollowup({
                content: `Usunięto ${deleted} wiadomości.`,
                flags: 64
            });
        } catch (err) {
            console.error(err);

            await interaction.createFollowup({
                content: "Wystąpił błąd podczas usuwania wiadomości.",
                flags: 64
            });
        }
    }
});

bot.connect();
