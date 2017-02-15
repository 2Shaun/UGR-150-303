#include <stdlib.h>
#include <stdio.h>
#include <math.h>						// unused

struct node{
	int x;
	struct node *next;
};

void buildList(struct node *emptyList, int divisor);
void findAndPrintPeriodicValues(struct node *function);

int main()
{

	struct node *head;
	head = malloc(sizeof(struct node));

	head->next = 0;
	struct node *pBuilder;
	pBuilder = head;
		
	buildList(head, 5);
	int i;
	if (pBuilder != 0)
	{
		while (pBuilder->next != 0)
		{
			printf("%d, ", pBuilder->x);
			pBuilder = pBuilder->next;
		}
	}		

	findAndPrintPeriodicValues(head);
	return 0;
}

void findAndPrintPeriodicValues(struct node *functionSet)
{
	struct node *tortoise;					// travels 1 node at a time
	struct node *hare;					// travels 2 nodes at a time
	tortoise = functionSet->next;					// start tortoise at 2nd node
	hare = functionSet->next->next;					// start hare at 3rd node


	while (tortoise->x != hare->x)
	{
		tortoise = tortoise->next;
		hare = hare->next->next;
	}
								// found period
								// this algorithm will only work as is only if it is assuredly a period
								// when they have found an equal element
	int mu;
	mu = 0;							// pre-periodic nodes
	tortoise = functionSet;					// restart the tortoise at 1st node
	while (tortoise->x != hare->x)
	{
		tortoise = tortoise->next;			// tortoise and hare travel at same speed
		hare = hare->next;
		mu++;						// count pre-periodic nodes
	}
	printf("\n first periodic node: %d ", tortoise->x);	// first periodic value
	int lambda;
	lambda = 1;						// periodicity
	hare = tortoise->next;					// set hare to 2nd periodic node
	while (tortoise->x != hare->x)				  
	{
		hare = hare->next;
		lambda++;					// count periodicity
	}
	
	printf("pre-periodic nodes: %d periodicity: %d\n", mu, lambda);
}

void buildList(struct node *emptyList, int divisor)
{
	struct node *listBuilder;
	listBuilder = emptyList;
	unsigned long long phi;					// phi(2^n)
	int i;
	phi = 2;						// start at 2
	for (i=1; i < 10; i++){
		phi = pow(phi, 2);				// raise previous phi to 2nd power and set it to phi
								// need to overwrite pow function
								// doubles are not big enough
		listBuilder->x = phi % divisor;
		listBuilder->next = malloc(sizeof(struct node));
		if (listBuilder == 0){
			printf("Out of memory.");
			break;
		}
		listBuilder = listBuilder->next;
	}
}
