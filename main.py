import json
import dice
from distee.webhook_client import WebhookClient
from distee.interaction import Interaction
from distee.application_command import ApplicationCommand, ApplicationCommandOption
from distee.enums import ApplicationCommandType, ApplicationCommandOptionType, IntegrationType, InteractionContextType


with open('config.json') as _f:
    cfg = json.load(_f)

client = WebhookClient()


async def on_roll(interaction: Interaction):
    d = interaction.data.options[0]['value']
    try:
        result = dice.roll(d)
        if len(result) > 1:
            await interaction.send(f'{d}: **{str(result)}** (total: **{sum(result)}**)')
        else:
            await interaction.send(f'{d}: **{str(result)}**')
    except dice.DiceBaseException:
        await interaction.send(f'Invalid dice expression "{d}"', ephemeral=True)

ap = ApplicationCommand(name='roll',
                        description='Roll the dice',
                        type=ApplicationCommandType.CHAT_INPUT,
                        integration_types=[IntegrationType.GUILD_INSTALL, IntegrationType.USER_INSTALL],
                        contexts=[InteractionContextType.GUILD, InteractionContextType.BOT_DM, InteractionContextType.PRIVATE_CHANNEL])
ap.options = [
    ApplicationCommandOption(name='dice',
                             type=ApplicationCommandOptionType.STRING,
                             required=True,
                             description='The dice expression to roll')
]
client.register_command(ap, on_roll, True, None)


client.run(cfg['public_key'], cfg['port'], cfg['host'], cfg['token'])

