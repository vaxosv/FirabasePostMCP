from postmcp.types import PostCreate, PostFilter, PostUpdate


class TestPostCreate:
    def test_valid_post(self):
        post = PostCreate(title="Test", content="<p>Hello</p>", description="A test post")
        assert post.title == "Test"
        assert post.slug == ""
        assert post.views30 == 0

    def test_title_too_long(self):
        import pydantic
        try:
            PostCreate(title="x" * 201, content="body", description="desc")
            assert False, "expected ValidationError"
        except pydantic.ValidationError:
            pass

    def test_empty_title(self):
        import pydantic
        try:
            PostCreate(title="", content="body", description="desc")
            assert False, "expected ValidationError"
        except pydantic.ValidationError:
            pass


class TestPostFilter:
    def test_defaults(self):
        f = PostFilter()
        assert f.limit == 20
        assert f.offset == 0

    def test_custom(self):
        f = PostFilter(category_id="abc123", tag="decor", limit=5)
        assert f.category_id == "abc123"
        assert f.tag == "decor"
        assert f.limit == 5


class TestPostUpdate:
    def test_all_optional(self):
        update = PostUpdate()
        assert update.model_dump(exclude_none=True) == {}

    def test_partial(self):
        update = PostUpdate(title="New title", slug="new-slug")
        assert update.title == "New title"
        assert update.content is None
