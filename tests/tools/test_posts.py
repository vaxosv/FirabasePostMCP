from postmcp.types import PostCreate, PostFilter, PostUpdate


class TestPostCreate:
    def test_valid_post(self):
        post = PostCreate(title="Test", content="Hello world")
        assert post.title == "Test"
        assert post.author == "AI"
        assert post.published is False

    def test_title_too_long(self):
        import pydantic
        try:
            PostCreate(title="x" * 201, content="body")
            assert False, "expected ValidationError"
        except pydantic.ValidationError:
            pass

    def test_empty_title(self):
        import pydantic
        try:
            PostCreate(title="", content="body")
            assert False, "expected ValidationError"
        except pydantic.ValidationError:
            pass


class TestPostFilter:
    def test_defaults(self):
        f = PostFilter()
        assert f.limit == 20
        assert f.offset == 0

    def test_custom(self):
        f = PostFilter(author="AI", limit=5, offset=10)
        assert f.author == "AI"
        assert f.limit == 5
        assert f.offset == 10


class TestPostUpdate:
    def test_all_optional(self):
        update = PostUpdate()
        assert update.model_dump(exclude_none=True) == {}

    def test_partial(self):
        update = PostUpdate(title="New title")
        assert update.title == "New title"
        assert update.content is None
