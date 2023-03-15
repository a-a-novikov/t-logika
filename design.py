from dataclasses import dataclass


@dataclass
class User:
    id: int
    gender: int
    preferred_gender: int
    age: int
    min_preferred_age: int
    max_preferred_age: int
    interests: list[str]


class Storage:

    def __init__(self):
        self.users_by_id: dict[int, User] = {}

    def create_user(
        self,
        user_id: int,
        gender: int,
        preferred_gender: int,
        age: int,
        min_preferred_age: int,
        max_preferred_age: int,
        interests: list[str],
    ) -> None:
        if user_id > 10**4:
            raise ValueError("'user_id' value is too big")

        if self.users_by_id.get(user_id):
            raise KeyError(f"user with id={user_id} already exists")

        if (gender or preferred_gender) not in [0, 1]:
            raise ValueError(f"'gender' must be 0 or 1 for male and female respectively")

        self.users_by_id[user_id] = User(
            user_id,
            gender,
            preferred_gender,
            age,
            min_preferred_age,
            max_preferred_age,
            interests,
        )

    def get_user_by_id(self, id_: int) -> User | None:
        return self.users_by_id.get(id_)

    def get_all_users(self) -> list[User]:
        return list(self.users_by_id.values())


class Tinder:

    def __init__(self):
        self.storage: Storage = Storage()

    def signup(
        self,
        user_id: int,
        gender: int,
        preferred_gender: int,
        age: int,
        min_preferred_age: int,
        max_preferred_age: int,
        interests: list[str],
    ) -> None:
        """
        Registers a user with the given attributes.
        """
        for _age in [age, min_preferred_age, max_preferred_age]:
            if _age < 18 or _age > 90:
                raise ValueError("age must be between 18 and 90")

        if len(interests) < 1 or len(interests) > 5:
            raise ValueError("user must have from 1 to 5 interests")

        invalid_interests = [i for i in interests if len(i) < 1 or len(i) > 20]
        if invalid_interests:
            raise ValueError("an interest must be from 1 to 20 symbols long")

        unique_interests = list(set(interests))

        self.storage.create_user(
            user_id,
            gender,
            preferred_gender,
            age,
            min_preferred_age,
            max_preferred_age,
            unique_interests,
        )

    def get_matches(self, user_id: int) -> list[int]:
        """
        Returns top 5 matches for the given user.
        """
        cur_user = self.storage.get_user_by_id(user_id)
        all_users = self.storage.get_all_users()
        all_users_without_cur = [i for i in all_users if i.id != cur_user.id]

        match_users = []
        for user in all_users_without_cur:
            if (
                cur_user.preferred_gender == user.gender
                and cur_user.min_preferred_age <= user.age <= cur_user.max_preferred_age
                and not set(cur_user.interests).isdisjoint(user.interests)
            ):
                match_users.append(user)
        sorted_by_relevance = self.__sort_matches_by_relevance(cur_user, match_users)
        return [u.id for u in sorted_by_relevance]

    @staticmethod
    def __sort_matches_by_relevance(user: User, matches: list[User]) -> list[User]:
        """
        Sort matched users by DESC common interests and ASC id.
        """
        return sorted(
            matches,
            key=lambda u: (len(set(user.interests).intersection(u.interests)), -u.id),
            reverse=True,
        )
