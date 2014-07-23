namespace py today
namespace php today

typedef i32 int
typedef string obj_id

struct User {
    1: int id
    2: string username
}

struct Post {
    1: int id
    2: string text
    3: User user
}

struct Comment {
    1: int id
    2: string text
}

service TodayInternalApiService
{
    int post_create(1: int user_id, 2: string text),

    Post post_get(1: int user_id, 2: int post_id),

    list <Post> post_list(1: int user_id),

    bool post_delete(1: int user_id, 2: int post_id),

    int post_comment_create(1: int user_id, 2: int post_id),

    list <Comment> post_comment_list(1: int user_id, 2: int post_id),

    bool post_comment_delete(1: int user_id, 2: int post_id, 3: int comment_id)
}
