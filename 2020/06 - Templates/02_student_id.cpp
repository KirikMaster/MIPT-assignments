bool operator==(const student& st1, const student& st2) {
    if (st1.id_number_string == st2.id_number_string) return 1;
    else return 0;
}