import disnake
from disnake.ext import commands
from typing import Optional

bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all(), activity=disnake.Game("Pulse", status=disnake.Status.online))



class TicketButtons(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = Optional[bool]

    @disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.red)
    async def confirm(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        if inter.author.guild_permissions.administrator:
            embed = disnake.Embed(title="Заявка отклонена", description=f"IP: `pulsemc.ru, Тикет удалится через 2 часа`", color=disnake.Colour.red())
            await inter.send(embed=embed)
            await inter.author.send("Ваша заявка была отклонена")
            self.value = True
            self.stop()

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green)
    async def close(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        if inter.author.guild_permissions.administrator:
            embed = disnake.Embed(title="Заявка одобрена", description="IP: `pulsemc.ru, Тикет удалится через 2 часа`", color=disnake.Colour.green())
            await inter.send(embed=embed)

            await inter.user.send("Ваша заявка была отклонена")
            self.value = True
            self.stop()

class MyModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Ваш ник",
                placeholder="Пример: Verfer_in",
                custom_id="Ник",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Возраст",
                placeholder="Пример: 15.",
                custom_id="Возраст",
                style=disnake.TextInputStyle.paragraph,
                max_length=3,
            ),
            disnake.ui.TextInput(
                label="О себе",
                placeholder="Пример: Я уже долго играю на серверах, разбираюсь в редстоуне",
                custom_id="О себе",
                style=disnake.TextInputStyle.short,
                max_length=300,
            ),
        ]
        super().__init__(
            title="Форма анкеты",
            custom_id="Заявка",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title=f"Анкета {inter.author.display_name}")
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1193239522083885137/1200008333214634084/Anketv_1.png?ex=65c49dd9&is=65b228d9&hm=e392c4caf41efd9088ebba1cd7dd51b88c59b7de8221c047909265da3ad404ef&")
        guild = inter.guild
        channel = await guild.create_text_channel(f"Тикет - {inter.user.display_name}")

        await channel.set_permissions(guild.default_role, view_channel=False)
        await channel.set_permissions(inter.user, view_channel=True)

        await inter.response.send_message(
            f"{inter.author.mention}, Вы создали тикет: Зайдите на него: {channel.mention}", ephemeral=True)

        view = TicketButtons()

        await channel.send(embed=embed, view=view)

class dropdown(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Бесплатная проходка", description="Напиши бесплатную проходку!", emoji="😀"),
            disnake.SelectOption(label="Платная проходка", description="Напиши платную проходку!", emoji="💵"),
            disnake.SelectOption(label="Видео заявка", description="Смонтируй видео заявку и отправь нам!", emoji="🎥"),
        ]
        super().__init__(
            placeholder="Выбрать вариант проходки",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        selected_option = self.values[0]
        if selected_option in ("Бесплатная проходка", "Платная проходка", "Видео заявка"):
            await inter.response.send_modal(modal=MyModal())

class DropDownView(disnake.ui.View):
    message: disnake.Message

    def __init__(self):
        super().__init__()
        self.add_item(dropdown())

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, (disnake.ui.Button, disnake.ui.BaseSelect)):
                child.disabled = True
        await self.message.edit(view=self)

@bot.event
async def on_ready():
    print("Бот готов к работе!")
    channel_id = 1200003325312122961
    channel = bot.get_channel(channel_id)
    if channel:
        view = DropDownView()
        embed = disnake.Embed(title="Выбери проходку", description="Это сделано для того чтобы отобрать только нормальных участников!", color=disnake.Colour.brand_green())
        embed.add_field(name="Варианты проходки:", value="Выберите один из вариантов")
        embed.add_field(name="1", value="Бесплатная проходка", inline=False)
        embed.add_field(name="2", value="Платная проходка", inline=False)
        embed.add_field(name="3", value="Видео заявка", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1193239522083885137/1200008333214634084/Anketv_1.png?ex=65c49dd9&is=65b228d9&hm=e392c4caf41efd9088ebba1cd7dd51b88c59b7de8221c047909265da3ad404ef&")
        embed.set_footer(text="Pulse 2023-2024")
        message = await channel.send(embed=embed, view=view)
        view.message = message
    else:
        print("Канал не найден")

token = ""
bot.run(token)
