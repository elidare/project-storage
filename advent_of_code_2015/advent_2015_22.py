# That took about 5 or 6 days, but thanks to this reddit comment
# https://www.reddit.com/r/adventofcode/comments/162ntk9/2015_day_22_part_2_golang_stuck_on_part_2_value/
# and the user Interesting_Fly_3396's golang solution https://pastebin.com/u85hecvv
# I eventually understood how I should solve it.
# Which I did! Wooohooo!

from collections import deque
import copy


class Boss:
    def __init__(self, damage=0, armor=0, hp=100):
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def is_dead(self):
        return self.hp <= 0

    def set_damage(self, damage):
        damage -= self.armor
        damage = damage if damage > 0 else 1
        self.hp -= damage


class Player(Boss):
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

    def get_mana_cost(self):
        return self.mana_cost

    def is_active(self):
        return self.timer > 0


class Game:
    def __init__(self, player, boss, spells, hard_level=False):
        self.player = player
        self.boss = boss
        self.spells = spells
        self.spell_chain = list()
        self.hard_level = hard_level

    def apply_player_attack(self):
        current_spell = self.spell_chain[-1]
        self.cast(current_spell)

    def apply_boss_attack(self):
        self.player.set_damage_through_armor(self.boss.damage, self.player.armor)

    def apply_effects(self):
        for sn, s in self.spells.items():
            match sn:
                case 'Shield':
                    self.player.armor = 7 if s.is_active() else 0
                case 'Poison':
                    if s.is_active():
                        self.boss.set_damage(3)
                case 'Recharge':
                    if s.is_active():
                        self.player.mana += 101

            s.decrement()

    def cast(self, spell):
        spell_obj = self.spells[spell]
        spell_obj.activate()
        self.player.mana -= spell_obj.get_mana_cost()
        self.player.mana_used += spell_obj.get_mana_cost()

        match spell:
            case 'MagicMissile':
                self.boss.set_damage(4)
            case 'Drain':
                self.boss.set_damage(2)
                self.player.hp += 2

    def decrease_player_hp(self):
        self.player.hp -= 1

    def next_spell(self, spell):
        self.spell_chain.append(spell)

    def get_possible_spells(self):
        possible_spells = list()
        for sn, s in self.spells.items():
            if not s.is_active() and s.mana_cost <= self.player.mana:
                possible_spells.append(sn)

        return sorted(possible_spells, key=lambda x: spells[x].mana_cost)

    def get_mana_used(self):
        return self.player.mana_used


spells = {
    'MagicMissile': Spell(53),
    'Drain': Spell(73),
    'Shield': Spell(113, 6),
    'Poison': Spell(173, 6),
    'Recharge': Spell(229, 5),
}


def play(level_hard=False):
    minimum_mana_cost = initial_mana_cost = 1_000_000
    player = Player(hp=50, mana=500)
    # Do not commit the real boss input
    boss = Boss(damage=8, hp=55)  # todo
    game = Game(player, boss, copy.deepcopy(spells), level_hard)

    queue = deque([game])

    while queue:
        current_game = queue.popleft()

        if current_game.get_mana_used() >= minimum_mana_cost:
            continue

        # Starting a player's turn
        if current_game.hard_level:
            current_game.decrease_player_hp()
            if current_game.player.is_dead():
                continue

        # Player's turn, applying effects
        current_game.apply_effects()
        if current_game.boss.is_dead():  # Only boss can die after applying effects
            minimum_mana_cost = min(minimum_mana_cost, current_game.get_mana_used())
            continue

        # Choose next spell to cast
        next_spells = current_game.get_possible_spells()

        if not len(next_spells):
            continue

        for sp in next_spells:
            new_game = copy.deepcopy(current_game)
            new_game.next_spell(sp)

            # Player is casting next spell
            new_game.apply_player_attack()

            # # Check if the boss is dead
            if new_game.boss.is_dead():
                minimum_mana_cost = min(minimum_mana_cost, new_game.get_mana_used())
                continue

            # Boss's turn, applying effects
            new_game.apply_effects()
            if new_game.boss.is_dead():
                minimum_mana_cost = min(minimum_mana_cost, new_game.get_mana_used())
                continue

            # Boss attacks
            new_game.apply_boss_attack()

            # If both player and boss are still alive, calculate further
            if not new_game.boss.is_dead() and not new_game.player.is_dead():
                queue.append(new_game)
            elif new_game.boss.is_dead():  # if the boss is dead, game over
                minimum_mana_cost = min(minimum_mana_cost, new_game.get_mana_used())

    return f'Minimum mana cost: {minimum_mana_cost}'


print(play())  # Part 1
print(play(True))  # Part 2, hard level
