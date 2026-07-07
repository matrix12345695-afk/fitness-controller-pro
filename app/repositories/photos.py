from sqlalchemy import select

from app.models.photo import Photo
from app.repositories.base import BaseRepository


class PhotoRepository(BaseRepository[Photo]):
    """
    Repository for answer photos.
    """

    async def get(
        self,
        photo_id: int,
    ) -> Photo | None:
        """
        Get photo by ID.
        """

        stmt = select(Photo).where(
            Photo.id == photo_id
        )

        return await self.scalar(stmt)

    async def create(
        self,
        answer_id: int,
        telegram_file_id: str,
    ) -> Photo:
        """
        Save telegram photo.
        """

        photo = Photo(
            answer_id=answer_id,
            telegram_file_id=telegram_file_id,
        )

        return await self.add(photo)

    async def get_by_answer(
        self,
        answer_id: int,
    ) -> list[Photo]:
        """
        Get all photos for answer.
        """

        stmt = (
            select(Photo)
            .where(
                Photo.answer_id == answer_id
            )
            .order_by(Photo.id)
        )

        return await self.scalars(stmt)

    async def get_last_photo(
        self,
        answer_id: int,
    ) -> Photo | None:
        """
        Get last uploaded photo.
        """

        stmt = (
            select(Photo)
            .where(
                Photo.answer_id == answer_id
            )
            .order_by(Photo.id.desc())
            .limit(1)
        )

        return await self.scalar(stmt)

    async def delete_photo(
        self,
        photo: Photo,
    ) -> None:
        """
        Delete photo.
        """

        await self.delete(photo)

        await self.commit()

    async def delete_all(
        self,
        answer_id: int,
    ) -> None:
        """
        Delete all photos of answer.
        """

        photos = await self.get_by_answer(
            answer_id
        )

        for photo in photos:
            await self.delete(photo)

        await self.commit()
