from collections import deque

# https://pastebin.com/u85hecvv
# https://www.reddit.com/r/adventofcode/comments/162ntk9/2015_day_22_part_2_golang_stuck_on_part_2_value/
# https://github.com/tomribbens/advent-of-code-tribbe


class Player:
    def __init__(self, damage=0, armor=0, hp=100):
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def is_alive(self):
        return self.hp > 0

    def set_damage(self, damage):
        damage -= self.armor
        damage = damage if damage > 0 else 1
        self.hp -= damage
        print('boss had', damage)

    # def get_current_stats(self):
    #     return self.damage, self.armor


class Wizard(Player):
    def __init__(self, damage=0, armor=0, hp=50, mana=500):
        super().__init__(damage, armor, hp)
        self.mana = mana

    # def get_current_stats(self):
    #     damage = 0
    #     armor = self.armor
        """
        Magic Missile costs 53 mana. It instantly does 4 damage.
    Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
    Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
    Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
    Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
        """
        # if self.spells['Shield'].is_active():
        #     armor += 7
        #     self.spells['Shield'].decrement()
        # if self.spells['Poison'].is_active():
        #     damage += 3
        #     self.spells['Poison'].decrement()
        # if self.spells['Recharge'].is_active():
        #     self.mana += 101
        #     self.spells['Recharge'].decrement()
        #
        # return damage, armor

    def set_damage_through_armor(self, damage, armor):
        damage -= armor
        damage = damage if damage > 0 else 1
        self.hp -= damage

    # def cast_and_get_instant_damage(self, spell):  # cast_and_get_instant_damage
    #     print('CAST:', spell)
    #     damage = 0
    #     if self.spells[spell].mana_cost <= self.mana:
    #         self.mana -= self.spells[spell].activate()
    #         if spell == 'MagicMissile':
    #             damage = 4
    #         elif spell == 'Drain':
    #             damage = 2
    #             self.hp += 2
    #     else:
    #         print('Not enough mana')
    #     return damage


class Spell:
    def __init__(self, mana_cost, lasts=0):
        self.active = False
        self.timer = 0
        self.lasts = lasts
        self.mana_cost = mana_cost

    def decrement(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.active = False

    def activate(self):
        self.active = True
        self.timer = self.lasts
        return self.mana_cost

    def is_active(self):
        return self.active


def apply_effects():
    for sn, s in spells.items():
        match sn:
            case 'Shield':
                wizard.armor = 7 if s.is_active() else 0
            case 'Poison':
                if s.is_active():
                    boss.hp -= 3
            case 'Recharge':
                if s.is_active():
                    wizard.mana += 101

        s.decrement()


wizard = Wizard(hp=10, mana=250)
# Do not commit the real input
boss = Player(damage=8, hp=13)

spells = {
    'MagicMissile': Spell(53),
    'Drain': Spell(73),
    'Shield': Spell(113, 6),
    'Poison': Spell(173, 6),
    'Recharge': Spell(229, 5),
}
total_mana_cost = 0


def cast(spell):
    # check current mana whether it is enough
    # check (before) if this spell is not active atm
    mana_cost = spells[spell].activate()
    wizard.mana -= mana_cost

    match spell:
        case 'MagicMissile':
            boss.hp -= 4
        case 'Drain':
            boss.hp -= 2
            wizard.hp += 2

    return mana_cost


def apply_wizard_turn():
    print('_____wizard turn')
    # apply lasting effects if any
    apply_effects()
    # get wizard stats
    wizard_damage, wizard_armor = wizard.damage, wizard.armor
    print('wizard_damage, wizard_armor', wizard_damage, wizard_armor, 'wizard hp', wizard.hp)
    # get boss stats
    boss_damage, boss_armor = boss.damage, boss.armor
    print('boss_damage, boss_armor', boss_damage, boss_armor, 'boss hp', boss.hp)

    # cast a spell
    total_mana_cost += cast('Drain')
    # add up the mana used
    # check if the boss is dead

    # print('Wizards turn, casting', spell)
    # wizard_damage += wizard.cast_and_get_instant_damage(spell)
    # print('wizard_damage after cast', wizard_damage)
    # boss.set_hit(wizard_damage)


def apply_boss_turn():
    print('_______Bosses turn')
    # apply lasting effects if any
    apply_effects()
    # get wizard stats
    wizard_damage, wizard_armor = wizard.damage, wizard.armor
    print('wizard_damage, wizard_armor', wizard_damage, wizard_armor, 'wizard hp', wizard.hp)
    # get boss stats
    boss_damage, boss_armor = boss.damage, boss.armor
    print('boss_damage, boss_armor', boss_damage, boss_armor, 'boss hp', boss.hp)

    # attack the wizard
    # check if the wizard is dead
    # boss's turn
    # wizard.set_hit_through_armor(boss_damage, wizard_armor)


def get_game_state():
    return f'Wizard: hp {wizard.hp}, mana {wizard.mana}, Boss: {boss.hp}'


def play():

    turn = 1
    queue = deque(['Poison', 'MagicMissile'])
    while True:
        if turn % 2 != 0:
            apply_wizard_turn()
        else:
            apply_boss_turn()

        turn += 1

        if turn == 4:
            break

    return 'Not ready'


print(play())
