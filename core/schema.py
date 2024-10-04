import graphene
from graphene_django import DjangoObjectType
from django.core.exceptions import ObjectDoesNotExist

from core.models import Note, Group, Tag


class NoteType(DjangoObjectType):
    class Meta:
        model = Note

class GroupType(DjangoObjectType):
    class Meta:
        model = Group

class TagType(DjangoObjectType):
    class Meta:
        model = Tag

class Query(graphene.ObjectType):
    all_notes = graphene.List(NoteType)
    note = graphene.Field(NoteType, id=graphene.Int(required=True))

    def resolve_all_notes(self, info):
        return Note.objects.all()

    def resolve_note(self, info, id):
        try:
            return Note.objects.get(pk=id)
        except Note.DoesNotExist:
            return None



class CreateNote(graphene.Mutation):

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        expiration_date = graphene.Date(required=False)
        group = graphene.Int(required=False)
        tags = graphene.List(graphene.Int, required=False)
        note_id = graphene.ID(required=True)

    note = graphene.Field(NoteType)

    def mutate(self, info, title, content, user_id, expiration_date=None, group_id=None, tag_ids=None):
        try:
            user = Note.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise Exception(f"User with id '{user_id}' does not exist.")

        note = Note.objects.create(
            title=title,
            content=content,
            expiration_date=expiration_date,
            user=user)


        if group:
            try:
                group = Group.objects.get(pk=group_id)
                note.group = group
            except ObjectDoesNotExist:
                raise Exception(f"Group with id '{group_id}' does not exist.")
        if tag_ids:
            tags = Tag.objects.filter(pk__in=tag_ids)
            note.tags.set(tags)

        note.save()
        return CreateNote(note=note)



class UpdateNote(graphene.Mutation):

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()
        expiration_date = graphene.Date()
        group_id = graphene.Int()
        tags_id = graphene.List(graphene.Int)

    note = graphene.Field(NoteType)

    def mutate(self, info, id, title=None, content=None, expiration_date=None, group_id=None, tag_ids=None):
        try:
            note = Note.objects.get(pk=id)
        except Note.DoesNotExist:
            raise Exception(f"Note with id '{id}' does not exist.")

        if title:
            note.title = title
        if content:
            note.content = content
        if expiration_date:
            note.expiration_date = expiration_date
        if group_id is not None:
            try:
                group = Group.objects.get(pk=group_id) if group_id else None
                note.group = group
            except ObjectDoesNotExist:
                raise Exception(f"Group with id '{group_id}' does not exist.")

        if tag_ids is not None:
            tags = Tag.objects.filter(pk__in=tag_ids)
            note.tags.set(tags)


        note.save()
        return UpdateNote(note=note)



class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()
    update_note = UpdateNote.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)