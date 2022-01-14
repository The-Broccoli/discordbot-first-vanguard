import discord
import re

class NameTags():
    def __init__(self) -> None:
        self.roleDic = {'Black Lotus': [
            '[BL]',
            r'[\[][bB][lL][\]]',
            {
                'BL': r'[B][L]',
                'Black Lotus': r'[bB][lL][aA][cC][kK][lL][oO][tT][uU][sS]'
            }
        ],
            'NW Gaming': [
            '[NWG]',
            r'[\[][nN][wW][gG][\]]',
            {
                'NWG': r'[nN][wW][gG]'
            }
        ]
        }

    async def magic(self, after: discord.ClientUser):
        for a_role in after.roles:
            for key in self.roleDic.keys():
                # Rolen Check
                if a_role.name in key:
                    # print(f'{after.display_name} hat die Rolle {key}')
                    relist = self.roleDic[key]
                    var1 = relist[1]  # R String des Ziel-Tags
                    var2 = relist[2]  # R Dic mit Verboten Namen
                    # Namen Check - 1 - Hat er schon denn Richting Tag in seinem Namen?
                    if re.search(var1, after.display_name):
                        # print(
                        #     f'{after.display_name} hat schon denn rechtigen Tag')
                        break
                    # Namen Check - 2 - Hat er einen Namen, der verboten ist?
                    for key in var2.keys():
                        # Hat er einen Namen Tag, der verboten ist?
                        if re.search(var2[key], after.display_name):
                            # print(
                            #     f'{after.display_name} hat {var2[key]} in seinem Namen')
                            new_name = after.display_name
                            new_name = re.sub(var2[key], '', new_name)
                            new_name. replace(' ', '')
                            # print(f'{after.display_name} wird zu {new_name}')
                            await after.edit(nick=new_name)
                            return
                    new_name = relist[0] + ' ' + after.display_name
                    await after.edit(nick=new_name)
                    return
        # remove @everyone
        rollen = after.roles[1:]
        # Hat er eine Rolle die wir behandeln? wenn ja  Abbruch
        for roll in rollen:
            for g in self.roleDic.keys():
                if roll.name == g:
                    return
        # Hat er keine Rolle die wir behandeln, werden erst
        # nach Tags gesucht und anschließend aus dem Namen
        # gelöscht
        for key in self.roleDic.items():
            if re.search(key[1][1], after.display_name):
                new_name = after.display_name
                new_name = re.sub(key[1][1], '', new_name)
                # print(f'Das ist der neue Name {new_name}')
                await after.edit(nick=new_name)
            else:
                # print(f'{after.display_name} is ok')
                pass