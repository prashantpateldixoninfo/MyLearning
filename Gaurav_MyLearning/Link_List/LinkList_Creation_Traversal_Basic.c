#include<stdio.h>
#include<stdlib.h>
struct node
{
    int data;
    struct node *next;
};

void traverse(struct node *ptr)
{
    do
    {
        printf(" data =%d\n ", ptr->data);
        ptr=ptr->next;
    }while(ptr->next!=NULL);
    printf(" data = %d\n", ptr->data);

    return;
}

struct node * insert_at_starting(struct node *head)
{   int value;
    struct node *ptr=(struct node *)malloc(sizeof(struct node));
    printf("\nEnter the data on the node=");
    scanf("%d",&value);
    ptr->data=value;
    ptr->next=head;
    return ptr;
}

struct node * insert_at_end(struct node *head)
{
    struct node *ptr=(struct node*)malloc(sizeof(struct node));
   // struct node *k=(struct node*)malloc(sizeof(struct node));
    struct node *p=head;
    int value;
    printf("\n Enter the new node data=");
    scanf("%d", &value);
    while(p->next!=NULL)
    {
        p=p->next;
    }
    p->next=ptr;
    ptr->next=NULL;
    ptr->data=value;
    return head;
}

struct node * insert_in_middle(struct node *head, int index)
{
    struct node *ptr=(struct node *)malloc(sizeof(struct node));
    struct node *temp=head;
    int value, k=2;
    printf("\nEnter the data of the node=");
    scanf("%d", &value);
    while(k< index)
    {
        temp=temp->next;
        k++;
    }
    ptr=temp->next;
    temp->next=ptr->next;
    free(ptr);
    return head;
}
struct node * insert_after_first_node(struct node *head)
{
    struct node * ptr=(struct node *)malloc(sizeof(struct node *));
    int value;
    printf("\nEnter the data in the node=");
    scanf("%d", &value);
    ptr->next=head->next;
    ptr->data=value;
    head->next=ptr;
    return head;
}
struct node *delete_first_node(struct node *head)
{
    struct node * ptr=head;
    head=head->next;
    free(ptr);
    return head;
    
}

struct node *delete_last_node(struct node*head)
{
    struct node *temp=(struct node *)malloc(sizeof(struct node));
    struct node *ptr=head->next;
    temp=head;
    while(ptr->next!=NULL)
    {   temp=temp->next;
        ptr=ptr->next;
    }
    temp->next=NULL;
    free(ptr);
    return head;
}

struct node *delete_middle_node(struct node* head, int ptr)
{
    struct node *new=head;
    struct node *new2=(struct node *)malloc(sizeof(struct node));
    int k=1;
    while(k<ptr-1)
    {
        new=new->next;
        k++;
    }
    new2=new->next;
    new->next=new2->next;
    free(new2);
    return head;
}

int main()
{
    struct node *head=(struct node *)malloc(sizeof(struct node));
    struct node *second=(struct node *)malloc(sizeof(struct node));
    struct node *third=(struct node *)malloc(sizeof(struct node));
    struct node *fourth=(struct node *)malloc(sizeof(struct node));

    head->data=6;
    head->next=second;
    
    second->data=10;
    second->next=third;

    third->data=11;
    third->next=fourth;
    
    fourth->data=15;
    fourth->next=NULL;
    traverse(head);
    printf("\n now the node is added to the starting of link list");
    head=insert_at_starting(head);
    traverse(head);
    printf("\nNow the node is added to the end of node\n");
    head=insert_at_end(head);
    traverse(head);
    head=insert_in_middle(head,5);
    traverse(head); 
    
    printf("\nnow the node is added after first node");
    head=insert_after_first_node(head);
    traverse(head);
    printf("\n deleting the middle 4 node");
    head=delete_middle_node(head, 4);
    traverse(head);
    printf("\ndeleting the first element=");
    head=delete_first_node(head);
    traverse(head);
    printf("\ndeleting the last node=");
    head=delete_last_node(head);
    traverse(head);
    return 0;
}
