# That took about 4 or 5 days, but thanks to this reddit comment
# https://www.reddit.com/r/adventofcode/comments/162ntk9/2015_day_22_part_2_golang_stuck_on_part_2_value/
# and the user Interesting_Fly_3396's golang solution https://pastebin.com/u85hecvv
# I eventually understood how I should solve it.
# Which I did! Wooohooo!
# TODO fix Part 2

from collections import deque
import copy


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
        # print(f'Boss has hit with {damage}')


class Wizard(Player):
    def __init__(self, damage=0, armor=0, hp=50, mana=500):
        super().__init__(damage, armor, hp)
        self.mana = mana
        self.mana_used = 0

    def set_damage_through_armor(self, damage, armor):
        damage -= armor
        damage = damage if damage > 0 else 1
        self.hp -= damage


class Spell:
    def __init__(self, mana_cost, lasts=0):
        self.timer = 0
        self.lasts = lasts
        self.mana_cost = mana_cost

    def decrement(self):
        if self.is_active():
            self.timer -= 1

    def activate(self):
        self.timer = self.lasts
        return self.mana_cost

    def is_active(self):
        return self.timer > 0


class Game:
    def __init__(self, wizard, boss, spells, hard_level=False):
        self.wizard = wizard
        self.boss = boss
        self.spells = spells
        self.spell_chain = list()
        self.wizard_win = None
        self.boss_win = None
        self.hard_level = hard_level

    def apply_wizard_turn(self):
        # print('_____wizard turn')
        if self.hard_level:
            self.wizard.hp -= 1
            if not self.wizard.is_alive():
                print('Wizard is dead by hp loss')
                self.boss_win = True
                return

        current_spell = self.spell_chain[-1]
        # get wizard stats
        # print(f'wizard damage {self.wizard.damage}, wizard armor {self.wizard.armor}, wizard hp {self.wizard.hp}, mana {self.wizard.mana}')
        # get boss stats
        # print(f'boss_damage {self.boss.damage}, boss_armor {self.boss.armor}, boss hp {self.boss.hp}')

        # apply lasting effects if any
        self.apply_effects()

        if not self.boss.is_alive():
            print('Boss is dead! Mana used', self.wizard.mana_used)
            self.wizard_win = True
            return

        # cast a spell
        # print('Wizards turn, casting', current_spell)
        self.wizard.mana_used += self.cast(current_spell)

        if not self.boss.is_alive():
            print('Boss dies, Player wins! Mana used', self.wizard.mana_used)
            self.wizard_win = True

    def apply_boss_turn(self):
        # print('_______Bosses turn')
        if self.hard_level:
            self.wizard.hp -= 1
            if not self.wizard.is_alive():
                print('Wizard is dead by hp loss')
                self.boss_win = True
                return

        # get wizard stats
        # print(f'wizard damage {self.wizard.damage}, wizard armor {self.wizard.armor}, wizard hp {self.wizard.hp}, mana {self.wizard.mana}')
        # get boss stats
        # print(f'boss_damage {self.boss.damage}, boss_armor {self.boss.armor}, boss hp {self.boss.hp}')

        # apply lasting effects if any
        self.apply_effects()

        if not self.boss.is_alive():
            print('Boss is dead! Mana used', self.wizard.mana_used)
            self.wizard_win = True
            return

        # boss attacks the wizard
        # print(f'Boss attacks with damage {self.boss.damage}, hits {self.boss.damage - self.wizard.armor}')
        self.wizard.set_damage_through_armor(self.boss.damage, self.wizard.armor)

        if not self.wizard.is_alive():
            # print('Wizard dies :(')
            self.boss_win = True

    def apply_effects(self):
        for sn, s in self.spells.items():
            match sn:
                case 'Shield':
                    self.wizard.armor = 7 if s.is_active() else 0
                case 'Poison':
                    if s.is_active():
                        self.boss.set_damage(3)
                case 'Recharge':
                    if s.is_active():
                        self.wizard.mana += 101

            s.decrement()

    def cast(self, spell):
        mana_cost = self.spells[spell].activate()
        self.wizard.mana -= mana_cost

        match spell:
            case 'MagicMissile':
                self.boss.set_damage(4)
            case 'Drain':
                self.boss.set_damage(2)
                self.wizard.hp += 2

        return mana_cost

    def next_spell(self, spell):
        # print('Append next spell to', self, self.spell_chain, spell)
        self.spell_chain.append(spell)

    def get_possible_spells(self):
        # print('Checking possible spells with mana', self.wizard.mana)
        possible_spells = list()
        for sn, s in self.spells.items():
            if not s.is_active() and s.mana_cost <= self.wizard.mana:
                possible_spells.append(sn)

        return sorted(possible_spells, key=lambda x: spells[x].mana_cost)

    def is_game_ended(self):
        return self.wizard_win or self.boss_win

    def get_mana_used(self):
        return self.wizard.mana_used


spells = {
    'MagicMissile': Spell(53),
    'Drain': Spell(73),
    'Shield': Spell(113, 6),
    'Poison': Spell(173, 6),
    'Recharge': Spell(229, 5),
}


def play(level_hard=False):
    minimum_mana_cost = initial_mana_cost = 1_000_000
    wizard = Wizard(hp=50, mana=500)
    # Do not commit the real boss input
    boss = Player(damage=8, hp=13)  # todo
    game = Game(wizard, boss, copy.deepcopy(spells), level_hard)

    queue = deque([game])

    while queue:
        current_game = queue.popleft()

        # Choose next spell to cast
        next_spells = current_game.get_possible_spells()

        if not len(next_spells):
            continue

        for sp in next_spells:
            new_game = copy.deepcopy(current_game)
            new_game.next_spell(sp)

            # Wizard's turn
            new_game.apply_wizard_turn()
            # Check if any player is dead
            if new_game.is_game_ended():
                if new_game.wizard_win:
                    minimum_mana_cost = min(minimum_mana_cost, new_game.get_mana_used())
                continue

            # Boss's turn
            new_game.apply_boss_turn()
            # Check if any player is dead
            if new_game.is_game_ended():
                if new_game.wizard_win:
                    minimum_mana_cost = min(minimum_mana_cost, new_game.get_mana_used())
                continue

            queue.append(new_game)

        # I sort the possible spells by their mana cost, ascending,
        # so I believe once I have found a situation where the Wizard defeats the Boss
        # this is a situation with minimum mana.
        # That reduces the script time vastly
        if minimum_mana_cost < initial_mana_cost:
            break

    return f'Minimum mana cost: {minimum_mana_cost}'


# print(play())
print(play(True))  # hard level
