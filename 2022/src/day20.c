#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>

#define NODE_COUNT 5000
#define DECRYPTION_KEY 811589153
#define MIX_COUNT 10

typedef struct Node Node;
struct Node {
    Node *prev;
    Node *next;
    long int value;
};

enum direction {
    left,
    right,
};

static void print_list(Node *zero) {
    int i = 0;
    Node *node = zero;
    while (i < NODE_COUNT){
        printf("%ld ", node->value);
        node = node->next;
        i++;
    }
    printf("\n");
}

static void rotate(Node *node, enum direction direction) {

    Node *prev = node->prev; /* old prev */
    Node *next = node->next; /* old next */

    switch (direction) {
    case left:
        node->prev = prev->prev;
        node->prev->next = node;

        next->prev = prev;
        prev->next = next;
        prev->prev = node;
        node->next = prev;
        break;

    case right:
        node->next = next->next;
        node->next->prev = node;

        prev->next = next;
        next->prev = prev;
        next->next = node;
        node->prev = next;
    }
}

int main(void) {
    FILE *fp = fopen("../inputs/day20", "r");
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    Node *nodes[NODE_COUNT];
    Node *zero;

    int i = 0;
    while ((read = getline(&line, &len, fp)) != -1) {
        long int value = atol(line) * DECRYPTION_KEY;
        printf("%ld\n", value);
        Node *node = (Node*) malloc(sizeof(Node));
        if (value == 0)
            zero = node;

        nodes[i] = node;
        node->value = value;
        i++;
    }

    nodes[0]->prev = nodes[NODE_COUNT - 1];
    nodes[0]->next = nodes[1];
    for (int i = 1; i < NODE_COUNT - 1; i++) {
        nodes[i]->prev = nodes[i-1];
        nodes[i]->next = nodes[i+1];
    }
    nodes[NODE_COUNT - 1]->prev = nodes[NODE_COUNT - 2];
    nodes[NODE_COUNT - 1]->next = nodes[0];

    long int value;
    for (int n = 0; n < MIX_COUNT; n++) {
        for (int i = 0; i < NODE_COUNT; i++) {
            Node *node = nodes[i];
            if ((value = node->value % (NODE_COUNT - 1)) > 0)
                while (value--)
                    rotate(node, right);
            else
                while (value++)
                    rotate(node, left);
        }
    }

    int xp = 1000 % NODE_COUNT;
    int yp = 2000 % NODE_COUNT;
    int zp = 3000 % NODE_COUNT;
    long int x,y,z;

    Node *node = zero;
    while (xp--)
        node = node->next;
    x = node->value;

    node = zero;
    while (yp--)
        node = node->next;
    y = node->value;

    node = zero;
    while (zp--)
        node = node->next;
    z = node->value;

    printf("sum = %ld\n", x + y + z);

    for (int i = 0; i < NODE_COUNT; i++) {
        free(nodes[i]);
    }
}
