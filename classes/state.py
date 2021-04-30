from __future__ import annotations
from abc import ABC, abstractmethod


class PetState(ABC):
    @property
    def pet(self):
        return self._pet

    @pet.setter
    def pet(self, pet) -> None:
        self._pet = pet

    @abstractmethod
    def update_state(self) -> None:
        pass


class Happy(PetState):
    def update_state(self) -> None:
        if self.pet.satiety < 50:
            self.pet.transition_to(Hungry())
        if self.pet.health < 50:
            self.pet.transition_to(Unhealthy())
        if self.pet.happiness < 90:
            self.pet.transition_to(Good())


class Died(PetState):
    def update_state(self) -> None:
        print("You died :(")


class Hungry(PetState):
    def update_state(self) -> None:
        if self.pet.health == 0 or self.pet.satiety == 0:
            self.pet.update(Died())
        if self.pet.satiety >= 50 and self.pet.health < 50:
            self.pet.transition_to(Unhealthy())
        if self.pet.satiety >= 50:
            self.pet.transition_to(Good())


class Unhealthy(PetState):
    def update_state(self) -> None:
        if self.pet.health == 0 or self.pet.satiety == 0:
            self.pet.update(Died())
        if self.pet.satiety < 50:
            self.pet.transition_to(Hungry())
        if self.pet.health >= 50:
            self.pet.transition_to(Good())


class Depression(PetState):
    def update_state(self) -> None:
        if self.pet.satiety < 50:
            self.pet.transition_to(Hungry())
        if self.pet.health < 50:
            self.pet.transition_to(Unhealthy())
        if self.pet.happiness > 0:
            self.pet.transition_to(Bad())


class Bad(PetState):
    def update_state(self) -> None:
        if self.pet.satiety < 50:
            self.pet.transition_to(Hungry())
        if self.pet.health < 50:
            self.pet.transition_to(Unhealthy())
        if self.pet.happiness <= 0:
            self.pet.transition_to(Depression())
        if self.pet.happiness >= 40:
            self.pet.transition_to(Boring())


class Boring(PetState):
    def update_state(self) -> None:
        if self.pet.satiety < 50:
            self.pet.transition_to(Hungry())
        if self.pet.health < 50:
            self.pet.transition_to(Unhealthy())
        if self.pet.happiness < 40:
            self.pet.transition_to(Bad())
        if self.pet.happiness >= 60:
            self.pet.transition_to(Good())


class Good(PetState):
    def update_state(self) -> None:
        if self.pet.happiness >= 90 and self.pet.health >= 90 and self.pet.satiety >= 90:
            self.pet.transition_to(Happy())
        if self.pet.satiety < 50:
            self.pet.transition_to(Hungry())
        if self.pet.health < 50:
            self.pet.transition_to(Unhealthy())
        if self.pet.happiness < 60:
            self.pet.transition_to(Boring())
