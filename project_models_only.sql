-- Project-specific schema (without Django internal and third-party app tables)

CREATE TABLE branches_branch (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20) NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE users_user (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP NULL,
    is_superuser BOOLEAN NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP NOT NULL,
    username VARCHAR(5) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    avatar VARCHAR(100) NULL,
    role VARCHAR(30) NOT NULL,
    balance INTEGER NOT NULL DEFAULT 0,
    branch_id BIGINT NULL REFERENCES branches_branch(id) ON DELETE SET NULL
);

CREATE TABLE courses_coursecategory (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE courses_course (
    id BIGSERIAL PRIMARY KEY,
    category_id BIGINT NOT NULL REFERENCES courses_coursecategory(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE lessons_lesson (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    lesson_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE groups_group (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    course_id BIGINT NOT NULL REFERENCES courses_course(id) ON DELETE CASCADE,
    branch_id BIGINT NOT NULL REFERENCES branches_branch(id) ON DELETE CASCADE,
    started_at DATE NOT NULL,
    ended_at DATE NULL,
    is_opened BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE groups_groupteacher (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL REFERENCES groups_group(id) ON DELETE CASCADE,
    teacher_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE
);

CREATE TABLE groups_groupstudent (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL REFERENCES groups_group(id) ON DELETE CASCADE,
    student_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    joined_at DATE NOT NULL
);

CREATE TABLE groups_grouplesson (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL REFERENCES groups_group(id) ON DELETE CASCADE,
    lesson_id BIGINT NOT NULL REFERENCES lessons_lesson(id) ON DELETE CASCADE
);

CREATE TABLE attendance_attendance (
    id BIGSERIAL PRIMARY KEY,
    group_lesson_id BIGINT NOT NULL REFERENCES groups_grouplesson(id) ON DELETE CASCADE,
    student_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE homeworks_homework (
    id BIGSERIAL PRIMARY KEY,
    group_lesson_id BIGINT NOT NULL REFERENCES groups_grouplesson(id) ON DELETE CASCADE,
    file VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    deadline TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE homeworks_homeworksubmission (
    id BIGSERIAL PRIMARY KEY,
    homework_id BIGINT NOT NULL REFERENCES homeworks_homework(id) ON DELETE CASCADE,
    student_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    file VARCHAR(100) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status VARCHAR(25) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE exams_exam (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL REFERENCES groups_group(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP NOT NULL,
    allow_resubmission BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE exams_examsubmission (
    id BIGSERIAL PRIMARY KEY,
    exam_id BIGINT NOT NULL REFERENCES exams_exam(id) ON DELETE CASCADE,
    student_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    file VARCHAR(100) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    checked_by_id BIGINT NULL REFERENCES users_user(id) ON DELETE SET NULL,
    checked_at TIMESTAMP NULL
);

CREATE TABLE payments_payment (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    amount NUMERIC(12,2) NOT NULL,
    payment_type VARCHAR(25) NOT NULL,
    paid_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE gamification_xp (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    reason VARCHAR(40) NOT NULL
);

CREATE TABLE shop_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE shop_product (
    id BIGSERIAL PRIMARY KEY,
    category_id BIGINT NOT NULL REFERENCES shop_category(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    price INTEGER NOT NULL,
    image VARCHAR(100) NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE shop_order (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES shop_product(id) ON DELETE CASCADE
);
