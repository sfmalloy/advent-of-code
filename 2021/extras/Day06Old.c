/**
 * @file Day06.c
 * @author Sean Malloy
 * Advent of Code Day 6
 */
/*************************************************************/
// Includes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*************************************************************/
// Typedefs and structs
typedef struct Fish Fish;

struct Fish {
    Fish* prev;
    Fish* next;
    int time;
};

/*************************************************************/
// Constants
const size_t FILE_BUFFER = 601;

/*************************************************************/
// Function decls
Fish* read_input();

void cleanup(Fish* head);

/*************************************************************/

/**
 *      0 <-> 1 <-> 2 <-> 3
 */

int main() {
    Fish* head = read_input();

    size_t size = 0;
    for (int i = 0; i < 256; ++i) {
        Fish* prev = NULL;
        Fish* curr = head;
        Fish* tail = NULL;
        Fish* added = NULL;
        Fish* prev_added = NULL;

        size_t curr_size = 0;
        while (curr != NULL) {
            // fprintf(stderr,"%d ", curr->time);
            if (curr->time == 0) {
                curr->time = 7;

                added = malloc(sizeof(Fish));
                added->time = 8;
                added->next = NULL;
                if (prev_added != NULL)
                    prev_added->next = added;
                else
                    tail = added;
                curr_size += 1;
                prev_added = added;
            }
            curr->time -= 1;
            prev = curr;
            curr = curr->next;
            curr_size += 1;
        }
        // fprintf(stderr, "\n");
        size = size < curr_size ? curr_size : size;
        prev->next = tail;
    }

    printf("%lu\n", size);

    cleanup(head);
}

Fish* read_input() {
    FILE* file = fopen("inputs/Day06.in", "r");
    char input[FILE_BUFFER];
    fscanf(file, "%s", input);

    char* token = strtok(input, ",");
    Fish* head = malloc(sizeof(Fish));
    head->time = strtol(token, NULL, 10);
    head->prev = NULL;
    head->next = NULL;

    Fish* prev = head;
    Fish* curr = NULL;

    while ((token = strtok(NULL, ",")) != NULL) {
        curr = malloc(sizeof(Fish));
        // curr->prev = prev;
        curr->time = strtol(token, NULL, 10);
        curr->next = NULL;
        prev->next = curr;

        prev = curr;
        curr = curr->next;
    }

    fclose(file);

    return head;
}

void cleanup(Fish* head) {
    while (head != NULL) {
        Fish* next = head->next;
        head->prev = NULL;
        free(head);
        head = next;
    }
}
