import disnake
from disnake import CategoryChannel, TextChannel, MessageInteraction
from typing import Optional
from disnake.ext import commands
from disnake import Member, Role
import os

bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all(), activity=disnake.Game("Pulse", status = disnake.Status.online))

class Ticket(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = Optional[bool]

    @disnake.ui.button(label="Нажми", style=disnake.ButtonStyle.blurple)
    async def confirm(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        guild = inter.guild

        channel = await guild.create_text_channel(f"Тикет - {inter.author.display_name}")

        embed = disnake.Embed(title="Вы создали тикет", description=f"Ticket channel: {channel.mention}",
                              color=disnake.Colour.green())
        await inter.send(embed=embed)
        self.value = True
        self.stop()
class AnimalDropdown(disnake.ui.StringSelect):
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
        guild = inter.guild

        # Создаем канал
        channel = await guild.create_text_channel(f"Тикет - {inter.author.display_name}")

        # Получаем роль администратора
        admin_role = disnake.utils.get(guild.roles, name="Администратор")

        # Устанавливаем права доступа для канала
        await channel.set_permissions(guild.default_role, view_channel=False)
        await channel.set_permissions(inter.author, view_channel=True)
        await inter.response.send_message(
            f"{inter.author.mention}, Вы создали тикет: Зайдите на него: {channel.mention}", ephemeral=True)

        if selected_option == "Бесплатная проходка":
            embed1 = disnake.Embed(title="Бесплатная проходка", description="Заполни пункты ниже")
            embed1.set_footer(text="Тест версия 1 ")
            embed1.add_field(name="1.", value="Ваш ник", inline=False)
            embed1.add_field(name="2.", value="Возраст", inline=False)
            embed1.add_field(name="3.", value="Кратко о себе", inline=False)
            embed1.set_image(
                url="https://cdn.discordapp.com/attachments/1193239522083885137/1200008333214634084/Anketv_1.png?ex=65c49dd9&is=65b228d9&hm=e392c4caf41efd9088ebba1cd7dd51b88c59b7de8221c047909265da3ad404ef&")
            await channel.send(embed=embed1)
        elif selected_option == "Платная проходка":
            embed2 = disnake.Embed(title="Платная проходка", description="Заполни пункты ниже")
            embed2.set_footer(text="Тест версия 1 ")
            embed2.add_field(name="1.", value="Ваш ник", inline=False)
            embed2.add_field(name="2.", value="Возраст", inline=False)
            embed2.set_image(
                url="https://cdn.discordapp.com/attachments/1193239522083885137/1200008333214634084/Anketv_1.png?ex=65c49dd9&is=65b228d9&hm=e392c4caf41efd9088ebba1cd7dd51b88c59b7de8221c047909265da3ad404ef&")
            await channel.send(embed=embed2)
        elif selected_option == "Видео заявка":
            embed3 = disnake.Embed(title="Видео заявка", description="Заполни пункты ниже")
            embed3.set_footer(text="Тест версия 1 ")
            embed3.add_field(name="1.", value="Ваш ник", inline=False)
            embed3.add_field(name="2.", value="Возраст", inline=False)
            embed3.add_field(name="3.", value="Ссылка на заявку, Ютуб/Диск/Файлом", inline=False)
            embed3.set_image(
                url="https://cdn.discordapp.com/attachments/1193239522083885137/1200008333214634084/Anketv_1.png?ex=65c49dd9&is=65b228d9&hm=e392c4caf41efd9088ebba1cd7dd51b88c59b7de8221c047909265da3ad404ef&")
            await channel.send(embed=embed3)


class DropDownView(disnake.ui.View):
    message: disnake.Message

    def __init__(self):
        super().__init__()
        self.add_item(AnimalDropdown())

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
        message = await channel.send(embed=embed, view=view)  # Отправляем сообщение в указанный канал
        view.message = message  # Устанавливаем сообщение для представления
    else:
        print("Канал не найден")



@bot.slash_command(description="Создать тикет")
async def ticket(inter):
    view = Ticket()

    await inter.response.send_message(f"Отправить тикет? ", view=view)

@bot.slash_command()
async def variants(inter: disnake.ApplicationCommandInteraction):
    view = DropDownView()
    embed = disnake.Embed(title="Выбери проходку", description="Это сделано для того чтобы отобрать только нормальных участников!", color=disnake.Colour.brand_green())
    embed.set_image(url="https://cdn.discordapp.com/attachments/1199819700465586279/1199985118077534248/4.png?ex=65c4883a&is=65b2133a&hm=0f146617f8bcca60bc8c1563c7a0214438997d13416dea39faa87c7d6651f9db&")
    embed.set_footer(text="Pulse 2023-2024")
    await inter.response.send_message(embed=embed, view=view)
    view.message = await inter.original_response()



token = ""

bot.run(token)
